from apps.AppBase import App
from apps.TimeApp import TimeApp
from collections.abc import Sequence



class AppCarousel():

    apps: Sequence[App]
    current_app_index: int

    curr: App
    
    def __init__(self, apps: Sequence[App]):
        
        self.apps = apps
        self.current_app_index = 0


    def render_current(self) -> bytes:

        curr = self.apps[self.current_app_index]

        if not curr.is_stale():
            curr.update()
        
        img_bytes = curr.render()
        self.advance_app()
        return img_bytes
    
    def advance_app(self):
        self.current_app_index = (self.current_app_index + 1) % len(self.apps)

    

