import click

from nailguard.detectors import get_detectors_names, get_detector
from nailguard.alerts import get_alerts_names, get_alert
from nailguard.nailguard import Nailguard


@click.command()
@click.option(
    "--detector",
    type=click.Choice(get_detectors_names()),
    multiple=True,
    default=["mediapipe"],
    help="Detector to use. Defaults to mediapipe."
)
@click.option(
    "--alert",
    type=click.Choice(get_alerts_names()),
    multiple=True,
    default=["beep"],
    help="Alerts to use. Defaults to notification, beep."
)
@click.option(
    "--camera",
    type=int,
    default=0,
    help="Camera index to use. Defaults to 0."
)
@click.option(
    "--trigger",
    type=int,
    default=1,
    help="Number of detectors which must trigger to alert. Defaults to 1."
)
@click.option(
    "--debounce",
    type=float,
    default=1.0,
    help="Number of second to wait before firing alert. Defaults to 1.0"
)
def main(detector: str, alert: list[str], camera: int, trigger: int, debounce: float):
    """Nailguard launcher"""
    
    detectors = [get_detector(detector) for detector in detector]
    alerts = [get_alert(alert) for alert in alert]
    Nailguard(detectors, alerts, camera, trigger, debounce).run()
