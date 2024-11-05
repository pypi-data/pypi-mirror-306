#!/usr/bin/python3

from miniquant_ioc.tau0.diode import EmissionTimeIOC
import asyncio, os, sys

from caproto.asyncio.server import run
from caproto.asyncio.server import Context as ServerContext

import logging
logger = logging.getLogger(__name__)

class Tau0Application:

    def __init__(self, prefix=None, args=None, env=None):

        if args is None:
            args = sys.argv.copy()

        if env is None:
            env = os.environ.copy()
        else:
            env.update(os.environ)

        self.prefix = prefix or env.get("RINGSYNC_EPICS_PREFIX", "KMC3:XPP:SYNC:")
        logger.info(f'Tau0 prefix: "{self.prefix}"')
        self.ioc_env = env
    
    async def async_run(self):
        async with EmissionTimeIOC(prefix=self.prefix,
                                   env=self.ioc_env) as ioc:
            self.ioc = ioc
            
            for pv in ioc.pvdb:
                logging.info(f"  {pv}")
            srv_ctx = ServerContext(ioc.pvdb)
            await srv_ctx.run()
