from pathlib import Path
from time import sleep

from notifypy import Notify

from .base import Alert


class NotificationAlert(Alert):
    
    def __init__(self):
        super().__init__()
        self.icon_path = str(Path(__file__).parent.parent / "assets" / "stop.png")
    
    def on_start(self):
        notification = Notify()
        notification.title = "Nailguard"
        notification.message = "Don't bite your nails!"
        notification.application_name = "Nailguard"
        notification.icon = self.icon_path
        notification.send()
