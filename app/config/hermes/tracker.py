# -*- coding: utf-8 -*-

'''

Hermes Config: Tracker

Holds configuration directives that apply to Tracker APIs, such as the `TrackerService`,
`PubSubService`, and others.

-sam (<sam.gammon@ampush.com>)

'''


config = {


    ## Tracker Service  
    'hermes.api.tracker.TrackerAPI': {
        'debug': False
    },


    ## Pub/Sub Service
    'hermes.api.tracker.PubSubAPI': {
        'debug': False
    }


}
