import cv2 as cv
from cv2 import imshow
import numpy as np
import create_lists as lists
from projection_finder import CalibrateCamera, ProjectPoints

if __name__ == '__main__':

    ##############FINAL:
    # 1: REPROJECT POINTS USING PROJECTPOINTS.
    # 2: COMPARE POINTS FROM METASHAPE AND PROJECTPOINTS.

        # DATA USED:
        # camera positions = from moving camera coordinates.
        # object points = from still target coordinates.
        # camera matrix = from still images.
        # pixels = from moving images.
        
    print("START FINAL\n")

    final_object_points= lists.TARGET_S_COORDINATES

    final_images= lists.MOVING_IMAGE_PATHS
    #final_camera=lists.CAMERA_M_COORDINATES
    #final_camera_matrix=lists.CAMERA_MATRIX
    #final_distortion_coefs=lists.DISTORTION_COEF
    #final_projectpoints=ProjectPoints(final_images,final_object_points,final_camera,final_camera_matrix,final_distortion_coefs)
    #final_projectpoints.create_projections()
    #print("IMAGE POINTS FROM FINAL_PROJECTPOINTS:\n")
    #print(final_projectpoints.projection_pixels)
    #FINAL_REPROJECTION_PIX=final_projectpoints.projection_pixels