#!/usr/bin/python3

from miniquant_ioc.histoview.nxsave import init_app
import logging, os, sys, asyncio
logger = logging.getLogger("miniquant-hsave")


def main(args=None, env=None):

    logging.basicConfig(level={
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'error': logging.ERROR
    }[os.environ.get('MINISAVER_LOGGING', 'info').lower()] )
    
    app = init_app(args or sys.argv, env or os.environ)
    asyncio.run(app.run())
    

if __name__ == "__main__":
    main()
