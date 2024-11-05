#!/usr/bin/python3

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time
import sys
import asyncio
from xarray import DataArray

#from caproto.sync import client as ca_client
#from caproto.sync import server as ca_server
from caproto.asyncio.client import Context

#from prometheus_client import start_http_server, Summary, Counter, Gauge

import argparse
import logging
import math
import xarray

from functools import partial

from emmi.ca.reader import GuidedAsyncReader, PvRetry

#from miniquant_ioc.hview_ioc import IOCRunner

class LiveDisplay:
    '''
    Uses Matplotlib to visualize numpy arrays (one or several?)
    '''
    
    def __init__(self, panels=None):
        '''
        Intialises a Matplotlib figure with the named panels.
        
        Parameters:
          - `panels`: A string array with panel reference names,
            or optionally a dictionary with reference and a displayable
            description.
        '''

        self.panelNames = panels or { "default": "Default display" }

        rows = int(round(math.sqrt(len(self.panelNames))))
        cols = int(math.ceil(len(self.panelNames)/rows))

        logging.info("Starting plotting interface")

        # We have a figure with NxM subplots (i.e. axes), each subplot hosting
        # one lineplot (for now), each referenced by name.
        self.figure = plt.figure()

        self.axes = { k: self.figure.add_subplot(rows, cols, i+1) for i,k in enumerate(self.panelNames) }
        
        #self.lines = { k: x.plot([])[0] for k, x in zip(self.panelNames, self.figure.axes) }

        # caching some data array metrics for autoscaling
        self.last_update = {k:time.time() for k in self.panelNames }
        
        self.figure.show(True)
        

    def update(self, panel, data=None, text=None, li=0, plot_dict=None, **plot_kwargs):
        ''' Updates data on the panel named `panel` using the data from `data`.

        Args:
            data: should preferrably be an `xarray.DataArray` container, in
                  which case all metadata will be used extracted from there.
        
            text: optional text to display in the axis.

            li: Line index, defaults to 0. Set this to something different than 0
              if more than one line are to be displayed within the same plot. Use
              a different value for each line then.

        The panels will upscale the X and Y ranges to fit all the data
        dynamics, but will never scale down.
        '''

        if data is None:
            return

        if not isinstance(data, DataArray):
            data = DataArray(data, coords=[range(len(data))], dims=["index"])

        if plot_dict is None:
            plot_dict = {}

        plot_dict.update(plot_kwargs)

        try:
            ax = self.axes[panel]
        except KeyError:
            logging.error("%s: no such display panel" % panel)
            return

        while li >= len(ax.lines):
            logging.info(f'Creating new plot in "{panel}"')
            ax.plot([], **plot_dict)

        xaxis = data.coords[next(iter(data.coords))].values
        
        xlim = np.array([xaxis[0], xaxis[-1]])
        if (xlim != ax.get_xlim()).all():
            logging.info("Adjusting X axis to %r" % xlim)
            ax.set_xlim(*xlim)

        ylim = ax.get_ylim()
        dlim = np.array([data.min(), data.max()])
        if (dlim[0] < ylim[0]) or (dlim[1] > ylim[1]):
            logging.info("Adjusting Y range to %r" % dlim)
            ax.set_ylim(min(dlim[0], ylim[0]), max(dlim[1], ylim[1]))

        #print(id(self.lines[panel]))
        #print(id(self.axes[panel].lines[0]))
        
        ax.lines[li].set_data(xaxis, data.values)
        
        self.figure.canvas.draw_idle()

        if text is not None:
            pass
            #text.set_text("acquisition: %2.2f Hz | flags: %r | counts: %d" % \
            #              (1.0/(tnow-t0),
            #               [], # f for f in hdev.flags
            #               data.sum()))

        
    def handle_events(self):
        self.figure.canvas.flush_events()


    async def loop(self, period=0.01):
        self.run_async_loop = True
        
        t0 = time.time()
        while self.run_async_loop:
            try:
                tdiff = time.time() - t0
                self.handle_events()
            except Exception as e:
                logging.error(str(e))
                raise
            await asyncio.sleep(period)


class ChannelDataDisplay:
    def __init__(self, prefix, channel):

        self.prefix=prefix
        self.channel=channel
        
        self.display = LiveDisplay(panels=['histo', 'rate'])

        self.display.axes['rate'].set_xlabel('Steps')
        self.display.axes['rate'].set_ylabel('Counts / second')

        self.display.axes['histo'].set_xlabel('Time (s)')
        self.display.axes['histo'].set_ylabel('Counts / acquisition')
        

    def handle_incoming(self, data, display_name=None):

        #print(f"Display: {data.keys()} -> {display_name}")

        if display_name is None:
            logging.warning(f'Display "{display_name}" doesn\'t exist')
            
        for i,(k,d) in enumerate(data.items()):
            print(f'Display to {display_name}: {type(d)}, {d.shape}')
            self.display.update(display_name, d, li=i, label=k)
        
        
        #self.display.update('histo', data[f'{self.prefix}CH{self.channel}_HISTOGRAM_SIGNAL'],
        #                    label=f'Channel {self.channel}')

    async def loop(self):
        await self.display.loop()


class FifoArrayWrapper:
    '''
    Quick 'n Dirty wrapper 
    '''
    def __init__(self, length, *args, **kw):
        self.data = np.zeros(length)

    def push_value(self, val):
        current = (self.data[1:]).copy()
        self.data[:-1] = current[:]
        self.data[-1] = val


class ScalarStackProcessor:
    ''' Loads a HydraHarp histogram and... does something with it.
    '''
    
    def __init__(self, var_name, stack_size=512):
        self.var_name = var_name
        self.var_stack = FifoArrayWrapper(stack_size)

        
    def handle_incoming(self, data):
        self.var_stack.push_value(data[self.var_name])
        return {
            f'{self.var_name}:stack': self.var_stack.data
        }
    

class DataPipeline:
    def __init__(self, reader):
        self.reader = reader
        self.reader.subscribe_incoming(self._accept_incoming)
        self.incoming_hooks = []
        
    def _accept_incoming(self, data):
        ''' This is where all the data from the reader enters the scene '''
        
        try:
            data_stack = [ data ]
            for hook_set in self.incoming_hooks:
                filter_proc = hook_set['filter']
                hook_procs = hook_set['procs']
                #print("Data:", data.keys())
                output = {k:v for k,v in data.items() if not filter_proc(k) }
                filtered_data = { k:v for k,v in data.items() if filter_proc(k) }
                #print("Filtered data:", filtered_data.keys())
                for hook in hook_procs:
                    try:
                        #print(f'{hook} on data {filtered_data.keys()}')
                        tmp = hook(filtered_data)
                        if tmp is not None:
                            output.update(tmp)
                        else:
                            logging.debug(f'Sink {hook} (no data output)')

                    except KeyError as e:
                        logging.error(f'Hook {hook} requested inexistent data: {str(e)}')
                    except Exception as e:
                        logging.error(f'Exception during hook {hook}: {str(e)}')
                        raise

                print("Pipeline step output:", output.keys())
                data_stack.append(output)
                data = output
                    
        except Exception as e:
            logging.error(f"DataPipeline: {str(e)}")
            raise
        

    def subscribe_incoming(self, *procs, filter=None):
        ''' We accept the same signature as reader incoming hooks (i.e.
        single parameter, data map), but also expect the incoming hook
        to actually return data back.

        Args:
            procs: List of incoming hook procedures (each accepts a data
              dictionary as parameter)

            filter: filter procedure to return True on every data key
              in the dictionary. Only data entries that pass this
              will be passed to the hook procedures.
        
        '''
        if filter is None:
            filter =  lambda k: True
        self.incoming_hooks.append({'procs': procs,
                                    'filter': filter})


class AcqTimeout(Exception):
    pass


class HarpAcqGuide:
    ''' Acquitition Guide driver for the Harp.

    If enabled (i.e. .loop() running on an async client context), it triggers
    a :ACQUISITIONVAL -> 1, then waits for :ACQUISITIONRBV -> 1, then -> 0,
    then starts again. In other words: it makes sure that the Harp is in
    perpetual acquisition.
    '''
    
    def __init__(self, harp_prefix, ctx=None):
        self.harp_prefix = harp_prefix
        self.ctx = ctx
        
    @property
    def acq_val_pv(self):
        return self.pvs[f'{self.harp_prefix}ACQUIRINGVAL']

    @property
    def acq_rbv_pv(self):
        return self.pvs[f'{self.harp_prefix}ACQUIRINGRBV']
   
    @property
    def acq_time_pv(self):
        return self.pvs[f'{self.harp_prefix}ACQUISITIONTIMERBV']

    
    async def wait_for(self, pv, proc, timeout=1.0):
        t0 = time.time()
        while not proc((await pv.read()).data[0]):            
            if (timeout is not None) and (time.time()-t0 > timeout):
                raise AcqTimeout()
            await asyncio.sleep(0.001)


    async def loop(self, ctx=None):
        
        if ctx is not None:
            self.ctx = ctx

        try:
            tmp = [
                f'{self.harp_prefix}ACQUIRINGVAL',
                f'{self.harp_prefix}ACQUIRINGRBV',
                f'{self.harp_prefix}ACQUISITIONTIMERBV',
            ]        
            self.pvs = { k:v for k,v in zip(tmp, await self.ctx.get_pvs(*tmp)) }

            while True:

                await self.acq_val_pv.write(1)

                try:
                    await self.wait_for(self.acq_rbv_pv, lambda v: v != 0, timeout=1.5)
                except AcqTimeout:
                    pass

                await self.wait_for(self.acq_rbv_pv, lambda v: v == 0, timeout=1.5)

                await asyncio.sleep(0.01)
                
        except Exception as e:
            logging.error(f"HarpAcqGuide: {str(e)}")
            raise


class Application:

    def __init__(self, opts):

        self.opts = opts

        data_pvs = [
            f"{opts.harp_prefix}CH{opts.channel}_HISTOGRAM_SIGNAL",
            f"{opts.harp_prefix}CH{opts.channel}_COUNTRATE",
            f"{opts.harp_prefix}SYNCRATE",
        ]

        guides = {
            f"{opts.harp_prefix}ACQUIRINGRBV": 0
        }

        self.data_processors = []

        # Data source
        self.reader = GuidedAsyncReader(ctx=None, pv=data_pvs, guides=guides)

        # The processing pipeline
        self.pipeline = DataPipeline(self.reader)
        
        if not self.opts.no_display:
            self.display = ChannelDataDisplay(self.opts.harp_prefix, self.opts.channel)

        # Step 1: plot histogram
        if hasattr(self, "display"):
            self.pipeline.subscribe_incoming(
                partial(self.display.handle_incoming, display_name="histo"),
                filter=lambda k: k.endswith("_HISTOGRAM_SIGNAL")
            )

        # Step 2: stack syncrates and countrate
        self.add_processors(
            ScalarStackProcessor(f'{opts.harp_prefix}SYNCRATE'),
            ScalarStackProcessor(f'{opts.harp_prefix}CH{opts.channel}_COUNTRATE'),
            filter=lambda k: not k.endswith("_HISTOGRAM_SIGNAL")
        )

        # Step 3: plot stacks
        if hasattr(self, "display"):
            self.pipeline.subscribe_incoming(partial(self.display.handle_incoming,
                                                     display_name="rate"))

        
        #
        # Experimental / non-processing stuff
        #
        if self.opts.guide:
            self.guide = HarpAcqGuide(self.opts.harp_prefix)


    #def add_sink(self, *sinks, filter=None,):
        

    def add_processors(self, *processors, filter=None):
        pprocs = []
        for p in processors:
            self.data_processors.append(p)
            pprocs.append(p.handle_incoming)
        self.pipeline.subscribe_incoming(*pprocs, filter=filter)
        
                
    async def loop(self):
        '''
        This is where the magic happens.
        '''

        self.client_ctx = Context()
        
        await self.reader.connect(self.client_ctx)

        if hasattr(self, "display"):
            self.display_task = asyncio.create_task(self.display.loop())

        if hasattr(self, "guide"):
            self.guide_task = asyncio.create_task(self.guide.loop(self.client_ctx))

        if hasattr(self, "ioc_runner"):
            self.ioc_runner_task = asyncio.create_task(self.ioc_runner.loop())

        while True:
            await asyncio.sleep(0.1)
            

def main():
    
    parser = argparse.ArgumentParser(prog="capeek", description="EPICS Channel Access data peek utility")
    parser.add_argument('-l', '--loglevel', action='store', default='INFO')
    #parser.add_argument('-p', '--mport', action='store', default=31415,
    #                    help='Port where to export summaries of data for Prometheus monitoring')
    parser.add_argument('-H', '--harp-prefix', action='store', default='KMC3:XPP:HARP:',
                        help='Prefix to use for all HydraHarp related variables')
    parser.add_argument('-c', '--channel', action='store', default=0,
                        help='Harp Channel to monitor')
    parser.add_argument('-g', '--guide', action='store_true',
                        help='Guide the acquisition')
    parser.add_argument('-n', '--no-display', action='store_true',
                        help='Don\'t bring up a Matplotlib display')
    parser.add_argument('-x', '--ioc', action='store_true',
                        help='Export generated data (IOCs, rates, ...) via an EPICS IOC')
    parser.add_argument('-r', '--roi', action='append', nargs=1,
                        help='Calculate a ROI sum for a region of WIDTH:CENTER (time axis coordinates)')

    opts = parser.parse_args()

    level = getattr(logging, (opts.loglevel or 'INFO').upper(), None)
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=level)

    app = Application(opts)
    
    #heartbeat = Counter((opts.ioc_prefix+opts.ioc_heartbeat).lower().replace(':', '_'),
    #                    'IOC master heartbeat for %s' % opts.ioc_prefix)

    #start_http_server(opts.mport)


    asyncio.run(app.loop())


if __name__ == "__main__":
    main()
