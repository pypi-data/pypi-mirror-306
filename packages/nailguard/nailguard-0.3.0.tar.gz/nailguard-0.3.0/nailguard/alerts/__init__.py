from .base import Alert
from .notification import NotificationAlert
from .beep import BeepAlert
from .screen import ScreenAlert

alerts = {
    "notification": NotificationAlert,
    "beep": BeepAlert,
    "screen": ScreenAlert,
}


def get_alerts_names() -> list[str]:
    return list(alerts.keys())


def get_alert(name: str) -> Alert | None:
    if name in alerts:
        return alerts[name]()
    return None
