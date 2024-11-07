#!/usr/bin/python3

from miniquant_ioc.reader import PvHistoReader
import time

import multiprocessing as mp
mp.set_start_method("spawn", force=True)

from caproto.asyncio.client import Context as ClientContext
from caproto.sync.client import read as ca_read
from caproto.sync.client import write as ca_write
from caproto import CASeverity

import pytest, asyncio, sys, os

class ReaderTestHelper:
    
    def __init__(self, harp_prefix, harp_channel):
        self.moo = None
        self.reader = PvHistoReader(harp_prefix, harp_channel)
        self.reader.subscribe_incoming(self.show_keys)
        self.reader.subscribe_incoming(self.show_shape)
        self.seen_keys = []
        self.histo_shape = None
    

    async def __aenter__(self):
        #
        # We need a general-purpose client (this one) and the reader
        # that follows the harp.
        #
        self.ctx = ClientContext()
        self.acq_auto, self.acq_time, self.acq_now, self.acq_set = \
            await self.ctx.get_pvs(
                f'{self.reader.harp_prefix}AUTO_ACQUIRE',
                f'{self.reader.harp_prefix}ACQUISITIONTIMERBV',
                f'{self.reader.harp_prefix}ACQUIRINGRBV',
                f'{self.reader.harp_prefix}ACQUIRINGVAL',
            )
        await self.reader.__aenter__()
        self.reader_task = asyncio.create_task(self.reader.read_loop())
        print('ReaderTestHelper: CA readers initialized')
        return self


    async def __aexit__(self, *a, **kw):
        print('ReaderTestHelper: tearing down CA readers')
        self.reader_task.cancel()
        try:
            await self.reader_task
        except asyncio.CancelledError:
            pass
        await self.ctx.disconnect()
        await self.reader.__aexit__()
        
        

    def show_keys(self, **data):
        print(f'Keys: {[k for k in data.keys()]}')
        self.seen_keys = [k for k in data.keys()]


    def show_shape(self, COUNTRATE, HISTOGRAM_SIGNAL, **kw):
        if HISTOGRAM_SIGNAL is None:
            return
        print(f'Shape: {HISTOGRAM_SIGNAL.shape}')
        self.histo_shape = HISTOGRAM_SIGNAL.shape


@pytest.mark.with_miniquant_ioc
class TestHistoread:

    async def test_histo(self, miniquant_ioc_instance, harp_prefix, harp_channel):

        async with ReaderTestHelper(harp_prefix, harp_channel) as h:

            print(f'HHelp: {h}')

            auto_on = (await h.acq_auto.read()).data[0]
            acq_time = (await h.acq_time.read()).data[0]
            
            print(f'AACQ: {auto_on}, every {acq_time} seconds (s)')

            t0 = time.time()
            tmax = 5.0 * acq_time
            while (time.time()-t0) <= tmax:

                acquiring = (await h.acq_now.read()).data[0]
                print(f'TestHistoread: {tmax-(time.time()-t0):1.0f} seconds to go, acquiring: {acquiring}')

                if not acquiring:
                    await h.acq_set.write(1)
                    acquiring = (await h.acq_now.read()).data[0]

                await asyncio.sleep(0.1)


            print(f'Seen: {h.seen_keys}')
            for k in [ "HISTOGRAM_SIGNAL", "COUNTRATE" ]:
                assert k in h.seen_keys
                
            assert h.histo_shape is not None
            assert len(h.histo_shape) == 1
