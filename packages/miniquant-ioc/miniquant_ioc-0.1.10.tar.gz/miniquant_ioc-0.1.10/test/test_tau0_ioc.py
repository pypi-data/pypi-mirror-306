#!/usr/bin/python3

from miniquant_ioc.tau0.main import main as init_ioc
import time

import multiprocessing as mp
#mp.set_start_method('fork')

from caproto.sync.client import read as ca_read, write as ca_write
from caproto.asyncio.client import Context as ClientContext
from caproto import CASeverity

import pytest, asyncio, sys, os

@pytest.mark.tau0_ioc
@pytest.mark.with_miniquant_ioc
class TestTau0Ioc:

    @pytest.fixture(scope='class')
    def tau0_ioc_instance(self, miniquant_ioc_instance, session_prefix,
                          harp_prefix, harp_channel):
        # returns: (process, prefix)

        print(f'Harp: {harp_prefix}')

        ioc_prefix = f'{session_prefix}:tau0:'
        ioc_args=None
        ioc_env={
            'RINGSYNC_EPICS_PREFIX': ioc_prefix,
            'RINGSYNC_HARP_PREFIX':  harp_prefix,
            'RINGSYNC_HARP_CHANNEL': harp_channel
        }

        print(f'Starting Tau0 test IOC...')
        
        p = mp.Process(target=init_ioc, args=[ioc_args, ioc_env])
        p.daemon = True
        p.start()
        print(f'Giving the IOC time to come up...')
        time.sleep(3)
        print(f'I guess we\'re moving: {p}')
        return p, ioc_prefix


    @pytest.mark.asyncio    
    async def test_pvs(self, tau0_ioc_instance, tau0_prefix):
        # without ...:ACQUISITIONTIMERBV the numbers will be nonsensical,
        # but the IOC should at least be responsive.

        ctx = ClientContext()
        
        pv_names = [ 'DIODE_T0', 'DIODE_TMAX' ]
        pv_objs = await ctx.get_pvs(*[f'{tau0_prefix}{p}' for p in pv_names ])
        
        for pn,po in zip(pv_names, pv_objs):
            d = await po.read()
            print(f'{pn} <- {d}')

        await ctx.disconnect()
