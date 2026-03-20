from datetime import datetime
from utils.TimeKeeper import now


class App():

    id:                 str
    name:               str
    enabled:            bool

    ttl:                float
    disp_duration:      float

    last_displayed:     float
    last_refreshed:     float

    config:             dict | None   #general purpose information

    def __init__(self, id, name, config = None, enabled = False, ttl = 60.0, disp_duration = 10.0):
        
        self.id = id
        self.name = name
        self.enabled = enabled
    
        self.ttl = ttl
        self.disp_duration = disp_duration
    
        self.last_displayed = 0.0
        self.last_refreshed = 0.0
    
        self.config = config

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def is_stale(self) -> bool:
        return (now() - self.last_refreshed) > self.ttl

    def update(self):
        raise NotImplementedError
    
    def render(self) -> bytes:
        raise NotImplementedError



