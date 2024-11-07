#!/usr/bin/python3

import logging
logger = logging.getLogger("tau0-ioc")

from miniquant_ioc.tau0.application import Tau0Application
import os, sys

import asyncio

def init_ioc(args=None, env=None):
    
    if args is None:
        args = sys.argv.copy()
        
    if env is None:
        env = os.environ.copy()
    else:
        env.update(os.environ)
     
    app = Tau0Application(args=args, env=env)
    return app


def main(args=None, env=None):

    #logging.basicConfig(level={
    #    'info': logging.INFO,
    #    'debug': logging.DEBUG,
    #    'warn': logging.WARNING,
    #    'warning': logging.WARNING,
    #    'error': logging.ERROR
    #}[os.environ.get('RINGSYNC_LOGGING', 'info').lower()] )
    
    asyncio.run(init_ioc(args or sys.argv, env or os.environ).async_run())


if __name__ == '__main__':
    main()
