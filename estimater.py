import cv2
import json
import numpy as np
import os

from XNect.modules.inference_engine_pytorch import InferenceEnginePyTorch
from XNect.modules.parse_poses import parse_poses

os.environ['KMP_DUPLICATE_LIB_OK']='True'

class Get_Pose_From_Webcam:

    def __init__(self, model = "./human-pose-estimation-3d.pth", GPU = True, camera_id = 0):

        if GPU is True:
            self.net = InferenceEnginePyTorch(model, 'GPU')
        else:
            print("Please Check NVIDIA CUDA is installed.")
            return

        self.model = model

        self.file_path = extrinsics_path = None
        if self.file_path is None:
            self.file_path = os.path.join('XNect\\data', 'extrinsics.json')
        with open(self.file_path, 'r') as f:
            self.extrinsics = json.load(f)
        self.R = np.array(self.extrinsics['R'], dtype=np.float32)
        self.t = np.array(self.extrinsics['t'], dtype=np.float32)

        self.capture = cv2.VideoCapture(camera_id)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.base_height = 256
        self.stride = 8
        self.fx = -1

    def rotate_poses(self, poses_3d, R, t):

        R_inv = np.linalg.inv(R)
        for pose_id in range(len(poses_3d)):
            pose_3d = poses_3d[pose_id].reshape((-1, 4)).transpose()
            pose_3d[0:3, :] = np.dot(R_inv, pose_3d[0:3, :] - t)
            poses_3d[pose_id] = pose_3d.transpose().reshape(-1)

        return poses_3d

    def estimate_poses(self):

        ret, frame = self.capture.read()
        current_time = cv2.getTickCount()
        if frame is None:
            return []
        input_scale = self.base_height / frame.shape[0]
        scaled_img = cv2.resize(frame, dsize=None, fx=input_scale, fy=input_scale)
        scaled_img = scaled_img[:, 0:scaled_img.shape[1] - (scaled_img.shape[1] % self.stride)]  # better to pad, but cut out for demo
        if self.fx < 0:  # Focal length is unknown
            self.fx = np.float32(0.8 * frame.shape[1])

        inference_result = self.net.infer(scaled_img)
        poses_3d, poses_2d = parse_poses(inference_result, input_scale, self.stride, self.fx, True)
        edges = []
        if len(poses_3d):
            #print("wow")
            poses_3d = self.rotate_poses(poses_3d, self.R, self.t)
            poses_3d_copy = poses_3d.copy()
            x = poses_3d_copy[:, 0::4]
            y = poses_3d_copy[:, 1::4]
            z = poses_3d_copy[:, 2::4]
            poses_3d[:, 0::4], poses_3d[:, 1::4], poses_3d[:, 2::4] = -z, x, -y

            poses_3d = poses_3d.reshape(poses_3d.shape[0], 19, -1)[:, :, 0:3]
            print(poses_3d)
            return poses_3d
        else:
            return []

"""
pose = Get_Pose_From_Webcam()
while True:
    pose.estimate_poses()

                #edges = (Plotter3d.SKELETON_EDGES + 19 * np.arange(poses_3d.shape[0]).reshape((-1, 1, 1))).reshape((-1, 2))
        #self.capture.release()
"""