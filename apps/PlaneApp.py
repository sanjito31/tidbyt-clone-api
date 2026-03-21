from apps.AppBase import App
from flights import flights_above
from utils.draw import draw_flight
from utils.TimeKeeper import now

class PlaneApp(App):

    cache: dict | None

    def __init__(self):
        super().__init__("plane", "Flights Above", ttl=60)
        
        self.cache = None


    def update(self):

        if self.cache and not self.is_stale(): return

        new_flight = flights_above()
        if new_flight is not None:
            self.cache = new_flight
        self.last_refreshed = now()


    def render(self):
        if self.is_stale(): self.update()

        if self.cache:
            return draw_flight(self.cache)
