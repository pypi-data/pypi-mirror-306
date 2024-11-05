#!/usr/bin/pyton3

from os import environ as env

if 'MINIQUANT_TEST' in env and env['MINIQUANT_TEST'] != 0:
    from miniquant import mock_harp as harp
else:
    from miniquant import harp

import logging
logger = logging.getLogger(__name__)

class HarpManager(object):
    '''
    Manages a Miniquant Harp device and its configuration presets.
    '''

    def __init__(self, device='first', startup=None, settings=None):
        self.harpDevice = device
        self.harp = harp.Monster().find(self.harpDevice)
        
        if startup:
            self.initialize(startup)

        if settings:
            self.configure(settings)

        self._aquisitionTime = 1.0


    def initialize(self, startup):
        '''
        Initializes the harp and runs a calibration measurement.
        The `startup` parameter is expected to contain a configuration
        dictionary with the following startup settings:
        
          - `measurementMode`: one of the `miniquant.harp.MeasurementMonde` variables,
            as string (`Histogramming`, `T2`, `T3`, `Continuous`). The string is
            case sensitive, default is `Histogramming`.
        
          - `referenceClock`: one of the `miniquant.harp.ReferenceClock` values
            as string, i.e. `Internal` or `External`. Default is `Internal`.
        
        '''
        logger.info("Initializing harp, this will take a moment...")
        self.harp.initialize(getattr(harp.MeasurementMode, startup['measurementMode']),
                             getattr(harp.ReferenceClock, startup['referenceClock']))
        self.harp.calibrate()
        logger.info("Harp ready")


    def __obj_conf(self, device_object, config):
        '''
        '''
        for propKey in config:
            #logging.info("Property: %r" % propKey)
            try:
                #logging.info("Investigating %r.%s", device_object, propKey) 
                device_prop = getattr(device_object, propKey)
                if not propKey in [ 'channels' ]:#hasattr(device_prop, "__getitem__"):
                    # Handling a Harp property
                    logger.info ("%r.%s -> %r" % (device_object, propKey, config[propKey]))
                    setattr(device_object, propKey, config[propKey])
                else:
                    # Handling Channels
                    logger.info ("Channel: %r" % device_object)
                    for chdev,chconf in zip(device_prop, config[propKey]):
                        logger.info ("Descending into channel: %r" % chdev)
                        self.__obj_conf(device_object=chdev, config=chconf)
            except:
                logger.error("Failure setting property '%s' of %r" % (propKey, device_object))
                logger.error("Value is: %r" % (cfg[propKey]))
                raise
        


    def configure(self, settings):
        '''
        Configures the Harp using values from the dictionary `settings`.
        The dictionary may contain values for the `miniquant.harp.MonsterHarp`
        properties `syncDiv`, `syncCfd` (with `level` and `zerox` in a dictionary)
            `syncChannelOffset`, `histogramLength`, `binning`, `offset`
        
        It also accepts a `channels` key with an array of channel properties,
        containing `enabled`, `offset` and `cfd` (again with `level` and `zerox`).
        '''

        # __obj_conf() does the heavy lifting, this is essentially just
        # a user-safe frontend.
        #print ("Settings:", settings)
        self.__obj_conf(self.harp, settings)


    def logStatus(self):
        '''
        Rapid logging of current harp setup and status, for debugging and information.
        '''
        hdev = self.harp
        logger.info ("Histogram length: %r" % hdev.histogramLength)
        logger.info ("Base resolution: %r" % (hdev.baseResolution,))
        logger.info ("Real resolution: %r" % hdev.resolution)
        if hdev.binning is not None:
            logger.info (f"Histogram delta: {hdev.baseResolution[0]*(2**hdev.binning)}")
        else:
            logger.info (f"Histogram delta: n/a, binning reported as {hdev.binning}")
        logger.info ("Histogram reach: %r" % (hdev.resolution*hdev.histogramLength,))
        logger.info ("Sync rate: %r" % hdev.syncRate)
        logger.info ("Sync period: %r" % hdev.syncPeriod)
        logger.info ("Count rates: %r" % [ch.countRate for ch in hdev.channels])
        logger.info ("Warnings: %r" % [ w for w in hdev.warnings] )
        logger.info ("Flags: %r" % [ f for f in hdev.flags] )

