#!/usr/bin/python3

default_harp_config = {
    'epics': {
        'harpBase': {
            'exports': [   
                {
                    'recordType': 'signal',
                    'signal': {
                        'name': 'resolution',
                        'kind': "analog"
                    }
                },

                {
                    'recordType': 'signal',
                    'signal': {
                        'name': 'syncRate',
                        'kind': "analog",
                        'killOnError': True
                    },
                },

                {
                    'recordType': 'signal',
                    'signal': {
                        'name': 'syncPeriod',
                        'kind': "analog"
                    },
                },

                {
                    'recordType': 'property',
                    'property': {
                        'name': 'acquiring',
                        'kind': "switch",
                        'validator': {
                            'values': {
                                1: True,
                                0: False
                            },
                        },
                    },
                },

                {
                    'recordType': 'property',
                    'property': {
                        'name': 'acquisitionTime',
                        'kind': "analog"
                    },
                },

                {
                    'recordType': 'signal',
                    'signal': {
                        'name': 'flag_aqactive',
                        'access': 'flags.ACTIVE',
                        'kind': "analog"
                    }
                },
                
            ] # exports
        }, # harpBase
        
        'harpChannels': {
            'interfix': 'ch{}_',
            'exports': [
                {
                    'recordType': 'property',
                    'property': {
                        'name': 'enabled',
                        'kind': "switch"
                    },
                },
                {
                    'recordType': 'signal',
                    'signal': {
                        'name': 'countRate',
                        'kind': 'analog'
                    },
                },
                {
                    'recordType': 'signal',
                    'signal': {
                        'name': 'histogram',
                        'suffix': 'histogram_signal',
                        'kind': "waveform",
                        'create': {
                            'length': 65536,
                            'FTVL': 'ULONG'
                        },
                    },
                },
                {
                    'recordType': 'signal',
                    'signal': {
                        'name': 'offset',
                        'suffix': 'histogram_offset',
                        'kind': "analog"
                    },
                },
                {
                    'recordType': 'signal',
                    'signal': {
                        'name': 'harp.resolution',
                        'suffix': 'histogram_delta',
                        'kind': "analog"
                    },
                },
            ], # exports
        }, # harpChannels
        'defaults': {}
    },
    
    'harp': {
        'settings': {
            'histogramLength': 6,

            'channels': [
                { 'enabled': True },
                { 'enabled': False },
                { 'enabled': False },
                { 'enabled': False },
            ],
        },
        
        'init': {
            'measurementMode': 'Histogramming',
            'referenceClock': 'Internal'
        }
    },
    
}
