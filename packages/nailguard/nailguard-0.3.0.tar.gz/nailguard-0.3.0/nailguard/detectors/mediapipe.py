from time import sleep
import os
from contextlib import redirect_stdout, redirect_stderr

from PIL import Image
import mediapipe as mp
import numpy as np

from .base import Detector


class MediapipeDetector(Detector):
    
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.1
        )
        self.face_detection = mp.solutions.face_detection.FaceDetection(
            min_detection_confidence=1.0
        )
    
    def detect(self, image: Image) -> bool:
        sleep(0.5)
        with open(os.devnull, 'w') as fnull:
            with redirect_stdout(fnull), redirect_stderr(fnull):
                fingertips_positions = self._get_fingertips_positions(image)
                mouth_position, mouth_size = self._get_mouth_position_and_size(image)
                if mouth_position is None:
                    return False
                closest_distance = self._get_closest_distance(fingertips_positions, mouth_position)
                return closest_distance < mouth_size / 4

    def _get_fingertips_positions(self, image: Image):
        image_rgb = np.asarray(image)
        hands_result = self.hands.process(image_rgb)
        
        all_positions = []
        if hands_result.multi_hand_landmarks:
            for hand_landmarks in hands_result.multi_hand_landmarks:
                positions = [hand_landmarks.landmark[i] for i in [4, 8, 12, 16, 20]]
                positions = [(int(landmark.x*image.width), int(landmark.y*image.height)) for landmark in positions]
                all_positions.extend(positions)
                    
        return all_positions
    
    def _get_mouth_position_and_size(self, image: Image):
        image_rgb = np.asarray(image)
        face_result = self.face_detection.process(image_rgb)
        
        max_area = 0
        position = None
        size = None
        
        if face_result.detections:
            for detection in face_result.detections:
                bbox = detection.location_data.relative_bounding_box
                area = bbox.width * bbox.height
                if area > max_area:
                    max_area = area
                    pos = detection.location_data.relative_keypoints[3]
                    position = (int(pos.x*image.width), int(pos.y*image.height))
                    size = int(bbox.width * image.width)
                    
        return position, size

    def _get_closest_distance(self, points: list, point: tuple) -> float:
        min_dist = float('inf')
        for p in points:
            dist = np.linalg.norm(np.array(p) - np.array(point))
            min_dist = min(min_dist, dist)
        return min_dist
