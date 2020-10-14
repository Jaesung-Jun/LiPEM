"""
Reference : 
https://github.com/CalciferZh/minimal-hand/blob/911eab268342c3cdc08e80fd371cf6003ffd4bd6/capture.py

"""
import cv2
import numpy as np
from network.input_reader import VideoReader, ImageReader

class OpenCVCapture:
    
    def __init__(self):
        
        cap = cv2.VideoCapture(0)
        
    def read(self):
        
        flag, frame = self.cap.read()
        if not flag:
            return None
        return np.flip(frame, -1).copy() # BGR to RGB