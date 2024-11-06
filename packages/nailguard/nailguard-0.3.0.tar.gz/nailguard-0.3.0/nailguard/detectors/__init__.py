from .base import Detector
from .mediapipe import MediapipeDetector


detectors = {
    "mediapipe": MediapipeDetector
}


def get_detectors_names() -> list[str]:
    return list(detectors.keys())


def get_detector(name: str) -> Detector | None:
    if name in detectors:
        return detectors[name]()
    return None
