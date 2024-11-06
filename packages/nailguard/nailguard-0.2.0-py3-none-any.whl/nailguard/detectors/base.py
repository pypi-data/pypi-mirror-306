from abc import ABC, abstractmethod

from PIL import Image


class Detector(ABC):
    
    @abstractmethod
    def detect(self, image: Image) -> bool:
        pass
