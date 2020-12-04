import numpy as np

from modules.input_reader import VideoReader
from modules.draw import Plotter3d, draw_poses
from modules.parse_poses import parse_poses

def rotate_poses(poses_3d, R, t):
    R_inv = np.linalg.inv(R)
    for pose_id in range(len(poses_3d)):
        pose_3d = poses_3d[pose_id].reshape((-1, 4)).transpose()
        pose_3d[0:3, :] = np.dot(R_inv, pose_3d[0:3, :] - t)
        poses_3d[pose_id] = pose_3d.transpose().reshape(-1)

    return poses_3d

def get_3d_info(device = 0, openvino = False, video = 0, model):
    frame_provider = VideoReader(video)
    frame = frame_provider.get_frame()
    
    if openvino:
        from network.inference_engine_openvino import InferenceEngineOpenVINO
        net = InferenceEngineOpenVINO(model, device)
    else:
        from metwprl.inference_engine_pytorch import InferenceEnginePyTorch
        net = InferenceEnginePyTorch(model, device)
    
    inference_result = net.infer(scaled_img)
    poses_3d, poses_2d = parse_poses(inference_result, input_scale, stride, fx, is_video)

    if len(poses_3d):
        poses_3d = rotate_poses(poses_3d, R, t)
        poses_3d_copy = poses_3d.copy()
        x = poses_3d_copy[:, 0::4]
        y = poses_3d_copy[:, 1::4]
        z = poses_3d_copy[:, 2::4]
        poses_3d[:, 0::4], poses_3d[:, 1::4], poses_3d[:, 2::4] = -z, x, -y

        poses_3d = poses_3d.reshape(poses_3d.shape[0], 19, -1)[:, :, 0:3]
