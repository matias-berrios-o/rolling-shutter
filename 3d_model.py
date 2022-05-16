import cv2 as cv
from ast import Constant
from cv2 import calibrateCamera
import matplotlib.pyplot as plt

from create_lists import still_targets_xyz,moving_targets_xyz,moving_cameras_xyz,still_cameras_xyz


#CALIBRATE CAMERA
cv.calibrateCamera()

#distortion coeff
#camera matrix
cam_matrix=0
dist_coeff=0


#define coordinates 3D
obj_coordinates_still=still_targets_xyz
obj_coordinates_moving=moving_targets_xyz


camera_coordinates_still=still_cameras_xyz
camera_coordinates_moving=moving_cameras_xyz

#find coordinates 2D
    #i want to use the still target coordinates since they should be the most accurate and the position of the moving cameras.
rotation_vector=[]
translation_vector=[]

projection_pixels=cv.projectPoints(obj_coordinates_still,rotation_vector,translation_vector,cam_matrix,dist_coeff)


##how do i define where the camera is??????
#https://python.hotexamples.com/examples/cv2/-/projectPoints/python-projectpoints-function-examples.html
##https://github.com/radjkarl/imgProcessor/blob/master/imgProcessor/camera/PerspectiveCorrection.py