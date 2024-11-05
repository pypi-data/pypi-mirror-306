#!/usr/bin/python3

import pytest, random, string, os, time
from miniquant_ioc.application  import init_app as init_ioc
from caproto.sync.client import read as ca_read

import multiprocessing as mp

## This is to auotmatically start a miniquant mock-ioc, once use_miniquant_ioc
## tests are running. If this is started as part of _this_ process, we can
## only start one per session (limitation of pythonSoftIOC). If we start
## this in a subprocess, apparently we can start several.

def run_miniquant_ioc(prf):
    # This is a version that does a full "run", i.e. blocks.
    app, cmdline = init_ioc(prf, args=[])
    app.runIoc()


def start_miniquant_ioc(prf):
    # This only starts the IOC within the context of the current
    # process -- necessary in some test environments, e.g. Gitlab CI.
    app, cmdline = init_ioc(prf, args=[])
    app.startIoc()


@pytest.fixture(scope='class')
def miniquant_ioc_instance(harp_prefix):
    if os.environ.get('MINIQUANT_TEST', 'no') == 'yes':
        if os.environ.get('MINIQTEST_FORK_IOC', 'yes') == 'yes':
            print(f'Spawning miniquant_ioc mock-up: "{harp_prefix}"')
            p = mp.Process(target=run_miniquant_ioc, args=[harp_prefix])
            p.start()
            yield harp_prefix
            print(f'Tearing down miniquant_ioc mock-up: "{harp_prefix}"')
            p.kill()
            p.join()
        else:
            print(f'Invoking miniquant_ioc mock-up: "{harp_prefix}"')
            start_miniquant_ioc(harp_prefix)
            print(f'Mock-up running')
            yield harp_prefix
            print(f'Mock-up teardown -- nothing to do (?)')
    else:
        try:
            ca_read(f'{harp_prefix}AUTO_ACQUIRE').data[0]
        except Exception as e:
            print(f'Unit test needs a running miniquant-ioc instance (expected prefix: {harp_prefix})')
        yield None

##
## Define a number of useful (EPICS) prefixes to use while testing, and
## which are unlikely to collide with anything else in the system:
##
##  - session_prefix: this is a 6 (or so) letter string that all this
##    this test sessions's EPICS CVs have in front. Override with
##    MINIQTEST_SESSION_PREFIX.
##
##  - harp_prefix: prefix specifically for the miniquant_ioc, both in
##    the miniquant_ioc only test, and as preparation for other IOCs.
##    All miniquant-related EPICS reads will go here. This is essentially
##    always "{session_prefix}:harp:", when we're running a fake
##    miniquant-ioc, or we're reading this from $MINIQUANT_EPICS_PREFIX
##    otherwise.
##
##  - other (more or less) generic prefixes: tau0_prefix, prefix, ... are
##    built similar to the `harp_prefix`, and may or may not have a way
##    to override. (Generally, they're built by appending a known string
##    to `session_prefix`, so overriding is usually not a useful feature).
##
## To test HARP features, we also need a channel in addition to a prefix.
## `harp_channel` exposes an integer we can use.
## 

@pytest.fixture(scope='session')
def session_prefix():
    p = ''.join(random.choice(string.ascii_lowercase) \
                for i in range(6))
    sp = os.environ.get('MINIQTEST_SESSION_PREFIX', p)
    print(f'Session IOC prefix: "{sp}"')
    return str(sp)


@pytest.fixture(scope='session', autouse=True)
def tau0_prefix(session_prefix):
    if os.environ.get('MINIQUANT_TEST', 'no') == 'yes':
        return f'{session_prefix}:tau0:'
    else:
        return os.environ.get("RINGSYNC_EPICS_PREFIX", "KMC3:XPP:SYNC:")


@pytest.fixture(scope='session', autouse=True)
def harp_prefix(session_prefix):
    if os.environ.get('MINIQUANT_TEST', 'no') == 'yes':
        return f'{session_prefix}:harp:'
    else:
        return os.environ.get("MINIQUANT_EPICS_PREFIX", "KMC3:XPP:HARP:")


@pytest.fixture(scope='session', autouse=True)
def harp_channel(session_prefix):
    if os.environ.get('MINIQUANT_TEST', 'no') == 'yes':
        return "0"
    else:
        return os.environ.get("MINIQTEST_HARP_CHANNEL", "0")


@pytest.fixture(scope='class')
def prefix(session_prefix):
    p = f'{session_prefix}:'+\
        ''.join(random.choice(string.ascii_lowercase) \
                for i in range(6))
    print(f'Class IOC prefix: "{p}"')
    return f'{p}'

