import cv2
import random
import string

class System:
    def __init__(self, settings):
        self.input_option = settings["input_option"]
        self.method = settings["method"]

