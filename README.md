# ipre

Files:

.txt files containing xyz positions of targets y cameras in meters.
  - `moving_targets_xyz_est`
  - `moving_cameras_xys_est`
  - `still_targets_xyz_est`
  - `still_cameras_xys_est`

Codigo:
  - `create_lists`: Converts .txt files to lists in python.
  - `3d_model`: Creates 2D points from 3D points.
  
##`3d_model`
  
  class CalibrateCamera:
  
  - Receives images, image points and object points.
  - Obtains camera attributes: camera matrix, rotation vector, translation vector, and distortion coefficients.

  class ProjectPoints:
  
  - Receives object points, image points, images.
  - Instances a CalibrateCamera variable.
  - def `create_2D_projection` creates projected points on a 2D plane from 3D points and camera attributes.
  - def `projection_correction` distorts projected points to comply with different camera angles.
