import cv2 as cv
from ast import Constant
from cv2 import calibrateCamera
import matplotlib.pyplot as plt

from create_lists import still_targets_xyz,moving_targets_xyz,moving_cameras_xyz,still_cameras_xyz


#CALLIBRATE CAMERA
cv.calibrateCamera()

#distortion coeff
#camera matrix


#define coordinates 3D

#find coordinates 2D
rotation_vector=[]
translation_vector=[]
obj_coordinates=still_targets_xyz
camera_coordinates=moving_cameras_xyz
projection_pixels=cv.projectPoints()
