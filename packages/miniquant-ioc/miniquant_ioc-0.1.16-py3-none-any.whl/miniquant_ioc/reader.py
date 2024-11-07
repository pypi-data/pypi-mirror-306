#!/usr/bin/python3

from caproto.asyncio.client import Context as ClientContext
from emmi.ca.reader import GuidedAsyncReader
from caproto import CaprotoTimeoutError

import asyncio, logging, time, traceback
logger = logging.getLogger(__name__)

class PvHistoReader:
    ''' Base class for guided reading of a Harp histogram signal.

    This is to be used when histograms are to be further processed
    data to be re-exported (see `miniquant_ioc.tau0.diode`, for
    instance).
    '''
    
    def __init__(self, harp_prefix=None, harp_channel=0, env=None):
        self.harp_prefix = harp_prefix or env.get("RINGSYNC_HARP_PREFIX", "KMC3:XPP:HARP:")
        self.harp_channel = harp_channel or env.get("RINGSYNC_HARP_CHANNEL", "0")
        self.pv_reader = self.__init_async_reader(self.harp_prefix)
        self._incoming_list = []
        self.pv_reader.subscribe_incoming(self._incoming)
        self.pre_incoming = None
        self.post_incoming = None
        self._processing = False
        self.do_run = True


    async def __aenter__(self, *a, **kw):
        logger.info(f'Creating CA client context')
        self.ca_client_ctx = ClientContext()
        await self.connect(self.ca_client_ctx)


    async def __aexit__(self, *a, **kw):
        if not hasattr(self, "ca_client_ctx"):
            logger.info(f'We don\t own a CA client')
            return
        await self.ca_client_ctx.disconnect()


    def _incoming(self, data):
        if len(data) == 0:
            return ## nothing to do yet

        self._processing = True
        d1 = { k.replace(self.harp_prefix, ''):v for k, v in data.items() }
        d2 = { k.replace(f'CH{self.harp_channel}_', ''):v for k, v in d1.items() }

        try:
            if hasattr(self.pre_incoming, "__call__"):
                self.pre_incoming()
        except Exception as e:
            logger.error(f'Error in pre-incoming hook: {e}: {traceback.format_exc()}')
            
        for p in self._incoming_list:
            try:
                p(**d2)
            except Exception as e:
                logger.error(f'Error in incoming hook: {e}: {traceback.format_exc()}')

        try:
            if hasattr(self.post_incoming, "__call__"):
                self.post_incoming()
        except Exception as e:
            logger.error(f'Error in post-incoming hook: {e}: {traceback.format_exc()}')

        self._processing = False
            

    def __init_async_reader(self, harp_prefix):
        return GuidedAsyncReader(
            ctx=None,
            prefix=harp_prefix,
            guides={ 'ACQUIRINGRBV': 1, },
            pv=[
                f'CH{self.harp_channel}_HISTOGRAM_SIGNAL',
                f'CH{self.harp_channel}_COUNTRATE',
                'SYNCRATE',
            ])


    async def connect(self, ctx=None):
        await self.pv_reader.connect(ctx)


    async def read_loop(self):
        self.do_run = True
        runtime_errors = 0
        while self.do_run:
            try:
                await asyncio.gather(*(self.pv_reader.wait_for_incoming(),
                                       asyncio.sleep(0.001)),
                                     return_exceptions=False)
            except RuntimeError as e:
                logger.error(f'Reading histogram: {e}, {traceback.format_exc()}')
                if runtime_errors == 0:
                    runtime_errors += 1
                    logger.error(f'If this is the only error, we\'ll ignore it')                    
                else:
                    logger.error(f'This seems to be reocurring -- bailing out')
                    raise

            except CaprotoTimeoutError as e:
                logger.error(f'Disconnected: {e}')

        
    def subscribe_incoming(self, proc):
        ''' Subscribes a new "incoming" proc.

        The general idea is that for every incoming histogram a procedure
        that receives the data.
        '''
        self._incoming_list.append(proc)
