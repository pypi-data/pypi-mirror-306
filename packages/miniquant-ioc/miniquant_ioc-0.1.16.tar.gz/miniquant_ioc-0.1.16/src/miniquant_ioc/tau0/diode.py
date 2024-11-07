#!/usr/bin/python3

from caproto.server import PVGroup, pvproperty
from caproto.asyncio.client import Context as ClientContext

import asyncio, logging, time
logger = logging.getLogger(__name__)

class AcqTimeout(Exception):
    pass

class EmissionTimeIOC(PVGroup):
    '''
    Drives a histogram acquisiton on a Harp IOC (via "...:ACQUSITIONVAL")
    and reads out the histogram on the corresponding channel to determine
    a time.

    The code is quite general, but comments and log messages are specific
    for the Laser/Ring synchronization.
    '''
    
    # Time at which the APP (laser diode) has seen the laser,
    # triggered by the ring frequency. This is the reference
    # time for synchonization.
    DIODE_T0 = pvproperty(value=0.0, doc="Laser-Ring reference time (via APD)")
    DIODE_TMAX = pvproperty(value=0.0, doc="Maximum T0 taken into account (a.k.a. histogram reach)")
    
    def __init__(self, *args, harp_prefix=None, harp_channel=0, env=None, **kwargs):

        self.harp_prefix = harp_prefix or env.get("RINGSYNC_HARP_PREFIX", "KMC3:XPP:HARP:")
        self.harp_channel = harp_channel or env.get("RINGSYNC_HARP_CHANNEL", "0")

        self.valid_t0 = None
        
        super().__init__(*args, **kwargs)

    async def __aenter__(self, *args, **kwargs):
        logger.info(f'Connecting to HARP PVs (args: {args}, kw: {kwargs})')
        self.harp_pvs = await self._get_harp_pvs(self.harp_prefix, self.harp_channel)
        return self


    async def __aexit__(self, *args, **kwargs):
        if hasattr(self, "ca_cli_ctx"):
            logger.info(f'HARP PV teardown (args: {args}, kw: {kwargs})')
            await self.ca_cli_ctx.disconnect()
        logger.info(f'HARP PV teardown IGNORED (args: {args}, kw: {kwargs})')
            

    async def wait_for(self, pv, proc, timeout=1.0):
        t0 = time.time()
        while not proc((await pv.read()).data[0]):            
            if (timeout is not None) and (time.time()-t0 > timeout):
                raise AcqTimeout()
            await asyncio.sleep(0.001)


    async def _get_harp_pvs(self, hpref, ch):
        ''' Returns a dictionary PVs for the necessary harp variables '''
        self.ca_cli_ctx = ClientContext()
        pv_def = {
            'acq_set':     f'{hpref}ACQUIRINGVAL',
            'acq_state':   f'{hpref}ACQUIRINGRBV',
            'acq_time':    f'{hpref}ACQUISITIONTIMERBV',
            'sync_rate':   f'{hpref}SYNCRATE',            
            'cnt_rate':    f'{hpref}CH{ch}_COUNTRATE',
            'histo':       f'{hpref}CH{ch}_HISTOGRAM_SIGNAL',
            'histo_delta': f'{hpref}CH{ch}_HISTOGRAM_DELTA',
            'histo_offs':  f'{hpref}CH{ch}_HISTOGRAM_OFFSET'
        }

        return {
            k:p for k,p in zip(
                pv_def.keys(),
                await self.ca_cli_ctx.get_pvs(*[
                    i[1]for i in  pv_def.items()
                ])
            )
        }

    
    async def _acquire_harp_t0(self, pv, tmax_pv):
        ''' Queries HARP and returns the APD t0.
        
        Uses the PVs from the `pv` dictionary (see self._get_harp_pvs() for access).
        Writes the t0 reach of the histogram to the `tmax_pv`.
        '''
        
        aqt = (await pv['acq_time'].read()).data[0]

        # request new acquisition
        await pv['acq_set'].write(1)

        # Wait for acquisition to start. But the HydraHarp is a brain-damaged
        # piece of hardware and takes about 1 second to respond to the
        # "start acquisition" API call. If the acquisition time is <1 second,
        # then we're hitting a timeout here before we even can realize that the
        # acquisition has started. If that happens, we just take it as it is
        # and assume this wait_for() was successful.
        try:
            await self.wait_for(pv['acq_state'], lambda v: v != 0, timeout=1.5)
        except AcqTimeout:
            pass

        # wait for acquisition to finish
        await self.wait_for(pv['acq_state'], lambda v: v == 0, timeout=aqt*3)

        h = (await pv['histo'].read()).data
        o = (await pv['histo_offs'].read()).data[0]
        d = (await pv['histo_delta'].read()).data[0]

        max_index = h.argmax()
        tau0 = o+max_index*d
        reach = o+d*len(h)

        await tmax_pv.write(value=reach)

        return tau0


    @DIODE_T0.startup
    async def DIODE_T0(self, inst, async_lib):
        ''' Read :CH0_HISTOGRAM_* and update tau0 value '''

        if hasattr(self, "harp_pvs"):
            pv = self.harp_pvs
        else:
            raise RuntimeError(f'You need to use this with "async with ..."')
        

        cnt = 0
        while True:

            try:
                
                t0 = await self._acquire_harp_t0(pv, self.DIODE_TMAX)

                cnt += 1

                if t0 == 0:
                    if self.valid_t0 != False:
                        r = (await pv['cnt_rate'].read()).data[0]
                        s = (await pv['sync_rate'].read()).data[0]
                        logger.warning(f'Diode T0 invalid!')
                        logger.warning(f'Count rate: {r}/s, sync rate: {s}/s')
                    self.valid_t0 = False
                else:
                    if self.valid_t0 is not True:
                        logger.info(f'Valid diode timing available: t0 = {t0} s')
                    self.valid_t0 = True

                if inst.value != t0:
                    await inst.write(value=t0)


            except AcqTimeout:
                logging.warn("Timeout while waiting for acquisition. Retrying.")
                await inst.write(value=0)
                await asyncio.sleep(1.0)
                
            except Exception as e:
                logging.error(str(e))
                logging.info("Will try again in 5 seconds...")
                await inst.write(value=0)                
                await asyncio.sleep(5)
