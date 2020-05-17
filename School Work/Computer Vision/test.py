from PIL import Image
import math
import numpy as np


class KeyPoint():
    def __init__(self, _location=(-1,-1), _scale=-1, _orientation=-1, _descriptor=[]):
        self.location = _location
        self.scale = _scale
        self.orientation = _orientation
        self.descriptor = _descriptor
    def __eq__(self, _other):
        self.location is _other.location


print(np.linalg.eig([[2, 0],[0, 3]]))