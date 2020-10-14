"""
This code is originally created by CalciferZh.
-> https://github.com/CalciferZh/minimal-hand
"""
import numpy as np

def xyz_to_delta(xyz, joints_def):
  """
  Compute bone orientations from joint coordinates (child joint - parent joint).
  The returned vectors are normalized.
  For the root joint, it will be a zero vector.

  Parameters
  ----------
  xyz : np.ndarray, shape [J, 3]
    Joint coordinates.
  joints_def : object
    An object that defines the kinematic skeleton, e.g. MPIIHandJoints.

  Returns
  -------
  np.ndarray, shape [J, 3]
    The **unit** vectors from each child joint to its parent joint.
    For the root joint, it's are zero vector.
  np.ndarray, shape [J, 1]
    The length of each bone (from child joint to parent joint).
    For the root joint, it's zero.
  """
  delta = []
  for j in range(joints_def.n_joints):
    p = joints_def.parents[j]
    if p is None:
      delta.append(np.zeros(3))
    else:
      delta.append(xyz[j] - xyz[p])
  delta = np.stack(delta, 0)
  lengths = np.linalg.norm(delta, axis=-1, keepdims=True)
  delta /= np.maximum(lengths, np.finfo(xyz.dtype).eps)
  return delta, lengths