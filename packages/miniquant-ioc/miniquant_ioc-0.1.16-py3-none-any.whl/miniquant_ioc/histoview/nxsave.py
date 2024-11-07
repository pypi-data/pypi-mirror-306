#!/usr/bin/python3

from miniquant_ioc.reader import PvHistoReader
from emmi.ca.format import PvStringFormatter
from caproto.asyncio.client import Context as ClientContext

from nx5d import ingest

import logging, os, sys, traceback

logger = logging.getLogger(__name__)

class HistoNxSaver:
    def __init__(self, harp_prefix=None, harp_channel=None,
                 instrument=None, sink_factory=None):
        ''' Initializes the `HistoNxSaver`, which saves histograms in HDF5-files.

        Args:
            harp_prefix: PV prefix of the miniqunt-ioc which serves the HydraHarp,
              (and from which we'll get our data)
        
            harp_channel: from which HydraHarp channel to read the data

            instrument: instrument name (as NXinstrument) to expect to find at
              `<group>` path. If not found, it is created. The data will be
              stored at `<group>/instrument/<instrument>/data`, and linked into
              `<group>/measurement/<instrument>`. The coordinate axes will
              also be stored, loosely in a NetCDF4-compatible format.

            sink_factory: callable with no arguments which will return an
              `nx5d.ingest` compatible `ScanSink` instance to save the data
              in.
        '''
        self.reader = PvHistoReader(harp_prefix, harp_channel)
        self.reader.subscribe_incoming(self.save)
        self.sink_factory = sink_factory
        self.nxinstr = instrument or f"harp-ch{harp_channel}"


    def save(self, **data):
        if self.sink_factory is None:
            logger.error(f'No scan sink available for saving')
            return

        try:
            self.scan_sink = self.sink_factory()
            self.scan_sink.append({ k.lower():v for k, v in data.items() })
            logger.info(f'To: {self.scan_sink.url} <- {[k.lower() for k in data.keys()]}')
        except Exception as e:
            logger.error(f'Error saving data: {e}, traceback: {traceback.format_exc()}')


    async def connect(self, ctx):
        self.ctx = ctx
        await self.reader.connect()


    async def run(self):
        await self.reader.read_loop()        


class NxSaverApplication:
    def __init__(self, args=None, env=None, h5format=None):
        ''' NxSaver application model.

        Args:
            args: application argument vector (typically `sys.argv`)
        
            env: env-vars (typically `os.environ`)

            h5format: Format string for building the HDF5 path at which
              to store the data. Once formatted, this will be passed on
              to `HistoNxSaver` every time it changes. The format key
              for this are being read from the environment variable
              `MINISAVER_H5PATH_ELEMENTS=<component1>[,<component2>[,...]]`.
              Here, each `<component>` has the format `<fmtkey>=<epicspv>`,
              where `<fmtkey>` is the keys to be used in `h5format`, and
              `<epicspv>` is an EPICS PV that will be constantly monitored
              in order to read out the data.
              If the format string here is `None`, it will be read from
              the environment variable `MINISAVER_H5PATH_FORMAT`. If it's
              missing or is an empty string, NxSaver will go through all
              the motions (for debugging), but will not do any saving.
        '''
        
        if args is None:
            args = sys.argv

        if env is None:
            env = os.environ
            
        self.harp_prefix = env.get('MINIQUANT_EPICS_PREFIX', 'KMC3:XPP:HARP:')
        self.harp_channel = env.get('MINISAVER_HARP_CHANNEL', '0')

        self._sink_formatter_elements = self._init_h5comp_dict(env.get('MINISAVER_H5PATH_ELEMENTS'))
        if 'scan' not in self._sink_formatter_elements:
            logger.warning(f'There is no \"scan\" key in $MINISAVER_H5PATH_ELEMENTS')
        
        self.h5formatter = PvStringFormatter(h5format or env.get('MINISAVER_H5PATH_FORMAT', ""),
                                             **(self._sink_formatter_elements))

        self.data_sink = None

        # FIXME: this will essentially make a sub-folder of any of the HARP
        # measurement data -- which is possibly not what we want. However,
        # this is what the API currently imposes. Need to fix that in a Nexus
        # compatible manner. (How?)
        #
        # FIXME: these are the same names as the ones in PvHistoReader
        # (just in lower-case). There needs to be a way to automatically access
        # them...
        self.harp_instrument_spec = {
            'histogram_signal': {
                'shape': (65536,),
                'dtype': int,
            },
            
            'syncrate': {
                'shape': tuple(),
                'dtype': int,
            },
            
            'countrate': {
                'shape': tuple(),
                'dtype': int,
            },

            'histogram_offset': {
                'shape': tuple(),
                'dtype': int,
            },

            'histogram_delta': {
                'shape': tuple(),
                'dtype': int,
            },

        }
        
        self.histosaver = HistoNxSaver(harp_prefix=self.harp_prefix,
                                       harp_channel=self.harp_channel,
                                       sink_factory=self._make_scan_sink)


    def _make_scan_sink(self):
        # Returns a H5ScanSink instance ready to accept data
        tmp = self.h5formatter.current
        if (self.data_sink) is None or (self.data_sink.url != tmp.strip('/')):
            self.data_sink = ingest.H5DataSink(h5like=tmp)

        try:
            return self.data_sink.open_scan(
                int(self.h5formatter.elements.get('scan', "0")),
                **self.harp_instrument_spec
            )
        except Exception as e:
            logger.error(f'Data sink with URL \"{self.data_sink.url}\" cannot provide means '
                         f'to save scan')
            logger.error(f'Reported: {e}')
            logger.error(f'Did you screw up $MINISAVER_H5PATH_FORMAT? (Have: '
                         f'"{os.environ.get("MINISAVER_H5PATH_FORMAT", "")}")')


    def _init_h5comp_dict(self, element_spec):
        ''' Returns a dictionary where the keys are h5path format keys, and elements are PVs. '''
        cd = {}
        
        if element_spec is None or len(element_spec)==0:
            logger.error(f'No HDF5 path elements in {element_spec}')
            return cd
        
        try:
            for comp in element_spec.split(','):
                k, v = comp.split('=')
                cd[k] = v
            return cd
        except Exception as e:
            logger.error(f'Error parsing: "{element_spec}". Expected format is `<key1>=<pv1>[,<key2>=<pv2>[,...]]`')
            raise


    async def run(self):
        self.ctx = ClientContext()
        await self.h5formatter.connect(self.ctx)
        await self.histosaver.connect(self.ctx)

        logger.info(f'Waiting for histograms')
        await self.histosaver.run()


def init_app(args=None, env=None):

    if args is None:
        args = os.argv
    if env is None:
        env = os.environ
    
    return NxSaverApplication(args, env)
    
