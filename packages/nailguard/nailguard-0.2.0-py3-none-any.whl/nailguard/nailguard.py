import threading
from time import sleep

import cv2
from PIL import Image
from nailguard.detectors import Detector
from nailguard.alerts import Alert


IMAGE_READ_FPS = 5
ALERT_CHECK_FPS = 10
MASTER_DETECTOR_FPS = 10


class Nailguard:
    
    def __init__(
        self,
        detectors: list[Detector],
        alerts: list[Alert],
        camera_idx: int,
        trigger_count: int,
        debounce: float
    ) -> None:
        self.detectors = detectors
        self.alerts = alerts
        self.camera_idx = camera_idx
        self.trigger_count = trigger_count
        self.debounce = debounce
        
        self.image = None
        self.current_detected = {detector: False for detector in detectors}
        self.master_detected = False
    
    def run(self) -> None:
        threading.Thread(target=self._image_thread, args=(self,)).start()
        
        for detector in self.detectors:
            threading.Thread(target=self._detector_thread, args=(self, detector)).start()
            
        threading.Thread(target=self._master_detector_thread, args=(self,)).start()
        
        for alert in self.alerts:
            threading.Thread(target=self._alert_thread, args=(self, alert)).start()

    @staticmethod
    def _image_thread(nailguard) -> None:
        cap = cv2.VideoCapture(nailguard.camera_idx)
        while True:
            ret, image = cap.read()
            if not ret:
                raise Exception("Failed to capture image from camera")
            
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            nailguard.image = image
            sleep(1 / IMAGE_READ_FPS)
        
    @staticmethod
    def _detector_thread(nailguard, detector: Detector) -> None:
        while True:
            if nailguard.image is None:
                continue
            detected = detector.detect(nailguard.image)
            nailguard.current_detected[detector] = detected

    @staticmethod
    def _master_detector_thread(nailguard) -> None:
        master_detector_period = 1 / MASTER_DETECTOR_FPS
        detected_count = 0
        while True:
            detected = all(nailguard.current_detected.values())
            if detected:
                detected_count += 1
            else:
                detected_count = 0
            nailguard.master_detected = detected_count > nailguard.debounce / master_detector_period
            sleep(master_detector_period)

    @staticmethod
    def _alert_thread(nailguard, alert: Alert) -> None:
        sleep_time = 1 / ALERT_CHECK_FPS
        while True:
            alert.handle(nailguard.master_detected)
            if not nailguard.master_detected:
                sleep(sleep_time)
