from apps.AppBase import App
from utils.TimeKeeper import now
from utils.draw import draw_text, draw_time
from datetime import datetime
from pytz import timezone

class TimeApp(App):
    timezone: str
    format_str: str

    time_to_display: str

    def __init__(self, ttl = 60, disp_duration=10, timezone="US/Eastern", format_str="%-I:%M%p"):
        super().__init__(id="time", name="Time", enabled=True, ttl=ttl, disp_duration=disp_duration)
        
        self.timezone = timezone
        self.format_str = format_str

    def update(self):
        current_time = datetime.now(timezone(self.timezone))
        
        self.last_refreshed = now()
        self.ttl = 60 - current_time.second
        
        self.time_to_display = current_time.strftime(self.format_str)

    def render(self) -> bytes:
        if self.is_stale():
            self.update()
            
        return draw_time(self.time_to_display)