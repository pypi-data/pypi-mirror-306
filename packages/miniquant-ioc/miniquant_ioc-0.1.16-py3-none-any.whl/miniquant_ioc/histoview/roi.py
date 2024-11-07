#!/usr/bin/python3

from caproto.server import PVGroup, pvproperty
from caproto.asyncio.server import Context as ServerContext

import asyncio, logging, time

from os import environ

class HistoRoiIOC(PVGroup):
    ''' Exports statistics about a region of interest via EPICS.
    '''

    SUM = pvproperty(value=0.0, doc="ROI sum")
    CENTER = pvproperty(value=0.0, doc="ROI center on the time axis")
    WINDOW = pvproperty(value=0.0, doc="ROI window on the time axis")

    def __init__(self, *args, roi=(0,0), **kwargs):
        super().__init__(*args, **kwargs)

class IOCRunner:
    def __init__(self, prefix, rois):
        self.roi_iocs = [
            HistoRoiIOC(prefix=f"{prefix}ROI{nr}:", roi=roi)
            for nr, roi in enumerate(rois)
        ]
    
    async def loop(self):

        pvdb = {}
        for ioc in self.roi_iocs:
            pvdb.update(ioc.pvdb)

        for pv in pvdb:
            logging.info(f'Exporting: {pv}')

        ctx = ServerContext(pvdb)
        await ctx.run()
        
