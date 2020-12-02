import cv2
import json
import numpy as np
import os

from XNect.modules.inference_engine_pytorch import InferenceEnginePyTorch
from XNect.modules.parse_poses import parse_poses

class Get_Pose_From_Webcam:

    def __init__():
    
        self.model = "./human-pose-estimation-3d.pth"
        self.net = InferenceEnginePyTorch(model, 'GPU')

        self.file_path = extrinsics_path = None
        if file_path is None:
            file_path = os.path.join('XNect\\data', 'extrinsics.json')
        with open(file_path, 'r') as f:
            extrinsics = json.load(f)
        R = np.array(extrinsics['R'], dtype=np.float32)
        t = np.array(extrinsics['t'], dtype=np.float32)

        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        base_height = 256
        stride = 8
        fx = -1

    def rotate_poses(poses_3d, R, t):

        R_inv = np.linalg.inv(R)
        for pose_id in range(len(poses_3d)):
            pose_3d = poses_3d[pose_id].reshape((-1, 4)).transpose()
            pose_3d[0:3, :] = np.dot(R_inv, pose_3d[0:3, :] - t)
            poses_3d[pose_id] = pose_3d.transpose().reshape(-1)

        return poses_3d

    def main():
        ret, frame = capture.read()
        current_time = cv2.getTickCount()
        if frame is None:
            break
        input_scale = base_height / frame.shape[0]
        scaled_img = cv2.resize(frame, dsize=None, fx=input_scale, fy=input_scale)
        scaled_img = scaled_img[:, 0:scaled_img.shape[1] - (scaled_img.shape[1] % stride)]  # better to pad, but cut out for demo
        if fx < 0:  # Focal length is unknown
            fx = np.float32(0.8 * frame.shape[1])

        inference_result = net.infer(scaled_img)
        poses_3d, poses_2d = parse_poses(inference_result, input_scale, stride, fx, True)
        edges = []
        if len(poses_3d):
            poses_3d = rotate_poses(poses_3d, R, t)
            poses_3d_copy = poses_3d.copy()
            x = poses_3d_copy[:, 0::4]
            y = poses_3d_copy[:, 1::4]
            z = poses_3d_copy[:, 2::4]
            poses_3d[:, 0::4], poses_3d[:, 1::4], poses_3d[:, 2::4] = -z, x, -y

            poses_3d = poses_3d.reshape(poses_3d.shape[0], 19, -1)[:, :, 0:3]
            print(poses_3d)
                #edges = (Plotter3d.SKELETON_EDGES + 19 * np.arange(poses_3d.shape[0]).reshape((-1, 1, 1))).reshape((-1, 2))
        capture.release()
        cv2.destroyAllWindows()