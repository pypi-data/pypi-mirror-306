#!/usr/bin/python3

from miniquant.harp import Monster
from miniquant.app import HarpManager

from emmi import app

from softioc import softioc, builder, asyncio_dispatcher
import asyncio

import sys, time
import numpy as np
import logging
logger = logging.getLogger(__name__)

from schema import SchemaError, Schema

from emmi.api.exports import ExportObjectFromDict, ActorConnector

from math import floor

import os
import argparse

from miniquant_ioc.config_example import default_harp_config

def loadFromYaml(path):
    from yaml import load, dump
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper

    return load(open(path, 'r').read(), Loader=Loader)
        
        
class HarpConnector(object):
    '''
    Will connect a Harp object (HarpManager, actually) to the EPICS CA protocol.

    Exports:
      - Waveform variables for the channels (with axis scaling)
      - a variable to switch preset proviles
      - a variable for setting histogram integration time
      - a variable for controlling data acquisition
    '''
    
    def __init__(self, iocDispatch, harpMan, epxHarp, epxChns, recTypeDefaults=None):
        '''
        Parameters:
          - `iocDispatch`: the pythonSoftIOC dispatcher to use
          - `harpMan`: the Harp manager
          - `epxHarp`: EPICS export configuration for the harp object
          - `epxChns`: EPICS export configuration for the channel objects.
          - `recTypeDefaults`: Dictionary that may contain sections with
            default parameters for each record type (e.g. `{"signal": "pollPeriod": ...}`)
        
        Both `epxHarp` and `epxChns` each have a section called "exports"
        which contains emmi "Connector Records" describing which
        fiels of the respective object get exported to EPICS under which
        suffix.

        The difference is that the `epxChns` dictionary also has supplementary
        information about intermediate naming schemes (as there are several
        channels, but only one Harp).
        '''
        
        self.iocDispatch = iocDispatch
        self.harpMan = harpMan
        self.recTypeDefaults = recTypeDefaults

        # Need to store a reference to some of the objects (e.g. the channels)
        # or they'll disappear.
        self.harp = harpMan.harp
        self.harp_channels = self.harp.channels

        # Support for auto-acquire PV: If this is set to True (as a PV),
        # then the HarpConnector will periodically trigger a re-acquire
        # every time the ACQUIRINGRBV is on 0.
        self.auto_acquire = False
        self.auto_acq_act = ActorConnector(ioc_dispatch=self.iocDispatch,
                                           suffix="AUTO_ACQUIRE",
                                           access=self.enableAutoAcq,
                                           kind="values",
                                           validator={'values': [0, 1]})
        self.iocDispatch(self.autoAcqLoop)

        logger.info("Exporting Harp base properties")
        if (epxHarp.get('exports') or None):
            self.exportEpics(self.harp, epxHarp['exports'])

        for i,ch in enumerate(self.harp_channels):
            if ch.enabled and (epxChns.get('exports') or None):
                logger.info("Exporting Harp properties for channel %d" % i)                
                self.exportEpics(ch, epxChns['exports'], interfix=epxChns['interfix'].format(i))
            else:
                logger.info("Ignoring disabled Harp channel %d" % i)


    def enableAutoAcq(self, val):
        # Enables auto-acquiring, i.e. resetting the "ACQUIREVAL" to 1 every
        # time it's on 0.
        logger.info(f'Auto-acquire: {val}')
        self.auto_acquire = bool(val)


    async def autoAcqLoop(self):
        while True:
            await asyncio.sleep(0.1)
            if not self.auto_acquire:
                continue
            if self.harpMan.harp.acquiring:
                continue
            self.harpMan.harp.acquiring = True


    def exportEpics(self, obj, spec, interfix=''):
        for rec in spec:
            logger.info("EPICS export of '%r' according to: %r" % (obj, rec))
            ExportObjectFromDict(self.iocDispatch, obj, rec,
                                 suffixMangle=lambda x: (interfix+x).upper(),
                                 recordTypeDefaults=self.recTypeDefaults)


class Application(app.IocApplication):
    '''
    Application model for a Miniquant IOC. Responsiblities:
      - managing a harp (indirectly)
      - shuffling configuration profiles (indirectly)
      - shuffling EPICS PVs
      - publishing the IOC.
    '''
    
    def __init__(self, cfg=None, **params):
        '''
        Parameters:
          - `cfg`: a configuration dictionary

        Any other named parameters passed to the constructor will be updated
        into the configuration dictionary.
        '''
        super().__init__(cfg=cfg)
        self.addFlatConfig(params, prefix='default')


    def setupHarp(self, devId=None):
        '''
        Initializes / creates a Harp device
        '''
        
        self.conf.setdefault('harp', {})
        if devId is not None:
            self.conf.setdefault['harp']['device'] = devId

        self.harpMan = HarpManager(self.conf['harp']['device'])

        start_preset = self.conf['harp']['settings'].get('fromPreset', '')
        
        self.pv['preset'] = self.iocBuilder.stringOut('preset', initial_value=start_preset,
                                                      on_update=self.harpReconfigure)
        
        self.harpMan.initialize(self.conf['harp']['init'])

        self.harpReconfigure(self.conf['harp']['settings'].get('fromPreset', ''))


    def harpReconfigure(self, preset):
        harp_settings = self.harpPreset(preset)
        self.harpMan.configure(harp_settings)
        self.harpMan.logStatus()


    def harpPreset(self, preset=None):
        '''
        Returns the Harp configuration preset named `preset`. If `None` is
        specified, returns the one that is set as default in the config file
        (configuration key `harp.settings`).

        Note that `harp.settings` may either have a `.fromPreset` field which
        must contain a preset name as string, or must contain Harp settings
        directly. Either way, if called with default parameter (`preset=None`),
        this function will return the set of settings referenced by or contained
        within `harp.settings`.
        '''

        if (preset is None) or (len(preset)==0):
            # direct settings under harp.settings
            logger.info("Using explicit Harp settings")
            presetDict = self.conf['harp']['settings']
            
        else:
            logger.info(f"Using Harp preset '{preset}'")
            
            # check out settings under prenamed preset; these either contain
            # a proper settings dicitonary, or they contain a 'fromFile' entry.
            pdata = list(filter(lambda x: x['name'] == preset, self.conf['harp']['presets']))[0]

            # FIXME: should valiade this with a schema?...

            try:
                base = os.path.dirname(self.conf['harp']['config'])
                pfile = os.path.join(base, pdata['fromFile'])
                presetDict = loadFromYaml(pfile)['settings']
                logger.info(f'Have presets from {pfile}')
            except KeyError:
                presetDict = pdata['settings']

        return presetDict


    def setupPvRecords(self):
        '''
        Sets up EPICS PV records
        '''
        self.harpCon = HarpConnector(self.iocDispatch, self.harpMan,
                                     self.conf['epics']['harpBase'],
                                     self.conf['epics']['harpChannels'],
                                     recTypeDefaults=self.conf['epics']['defaults'])

    
def init_app(prefix=None, args=None):

    ## FIXME: should move this into the Application class somehow, this
    ## no longer is the main() method...

    if args is None:
        args = sys.argv.copy()
    
    parser = argparse.ArgumentParser(prog='miniquant-ioc', description='EPICS-IOC for the HydraHarp 400')
    
    parser.add_argument('-d', '--harp-device', action='store', default='first',
                        help='HydraHarp device ID to use')
    
    parser.add_argument('-c', '--harp-config', action='store',
                        help='Load configuraion from YAML file')
    
    parser.add_argument('-s', '--harp-settings-fromPreset', action='store',
                        help='HARP settings preset to use')
    
    parser.add_argument('-l', '--logging', action='store',
                        help='Logging level')
    
    parser.add_argument('-e', '--epics-prefix', action='store',
                        help='EPICS prefix to export to')
    
    cmdline = parser.parse_args(args[1:])

    if cmdline.harp_config:
        logger.info("Config from file: %s" % cmdline.harp_config)
        ycfg = loadFromYaml(cmdline.harp_config)
    else:
        ycfg = default_harp_config

    miniApp = Application(default_epics_prefix=prefix or 'KMC3:XPP:HARP:', default_harp_device='first')
    miniApp.addFlatConfig({k:v for k,v in vars(cmdline).items() if v}, prefix="epics", subsection="epics")
    miniApp.addFlatConfig({k:v for k,v in vars(cmdline).items() if v}, prefix="harp", subsection="harp")
    miniApp.addNestedConfig(ycfg)
    miniApp.addFlatConfig(os.environ, prefix='MINIQUANT', subsection="harp")
    
    miniApp.setupIoc()
    miniApp.setupHarp()
    miniApp.setupPvRecords()

    return miniApp, cmdline
