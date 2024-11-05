#!/usr/bin/python3

import time

import multiprocessing as mp

from caproto.sync.client import read as ca_read, write as ca_write
from caproto import CASeverity

import pytest, asyncio, sys, os

@pytest.mark.with_miniquant_ioc
def test_ioc(miniquant_ioc_instance):

    print(f'Testing miniquant-ioc')

    prf = miniquant_ioc_instance

    pv = [ 'SYNCRATE', 'CH0_COUNTRATE' ]

    for s in pv:
        result = ca_read(f'{prf}{s}', timeout=30.0)
        data = result.data
        print(f'{prf}{s} -> {data}')
        
        assert len(data) > 0
