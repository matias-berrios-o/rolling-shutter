
import cv2 as cv
import numpy as np
import create_lists as lists
from projection_finder import CalibrateCamera, ProjectPoints

if __name__ == '__main__':

    ###############TEST 1: COMPARE CAMERA MATRIX AND DISTORTION COEFFICIENTS FROM OPENCV AND METASHAPE

    # 1: FIND PIXEL COORDINATES OF TARGETS IN CROPPED IMAGES WITH CALIBRATECAMERA.
    # 2: FIND CAMERA MATRIX, DISTORTION COEFFICIENTS AND CAMERA POSITIONS WITH CALIBRATECAMERA.
    # 3: FIND REPROJECTED PIXELS OF TARGETS WITH PROJECTPOINTS.
        # 3.1: USING CAMERA MATRIX AND DISTORTION COEFFICIENTS FROM METASHAPE.
        # 3.2: USING CAMERA MATRIX AND DISTORTION COEFFICIENTS FROM CALIBRATECAMERA.
    # 4: COMPARE PIXELS OBTAINED FROM (# 3).

        # DATA USED:
        # camera positions = from CalibrateCamera.
        # object points = from still target coordinates.
        # camera matrix and dist. coeff. = from CalibrateCamera.
        # camera matrix and dist. coeff. = from Metashape.
        # images = from cropped images.


    print("START TEST 1\n")

    folder_path1='photos/cropped_images/'
    test1_object_points= lists.TARGET_S_COORDINATES
    test1_images= lists.CROPPED_IMAGE_PATHS
    test1_camera_matrix=lists.CAMERA_MATRIX
    test1_distortion_coef=lists.DISTORTION_COEF
    test1_calibrate=CalibrateCamera(test1_images,test1_object_points)
    test1_calibrate.circles_grid_centers() #finds pixel coordinates for images
    test1_calibrate.calibrate() #finds camera matrix, dist. coefficients and camera rotation translation vectors for each image

    #check the camera matrix and d. coefficients lists to see if they are all the same, by default I am using the first ones.
    cam_matrix_opencv=test1_calibrate.cam_matrix[0]
    d_coefficients_opencv=test1_calibrate.d_coeff[]0
    test1_project_opencv=ProjectPoints(test1_images,test1_calibrate.image_points2,test1_object_points,test1_calibrate.camera_positions,cam_matrix_opencv,d_coefficients_opencv,folder_path1)
    test1_project_opencv.create_projections("opencv")

    test1_project_metashape=ProjectPoints(test1_images,test1_calibrate.image_points2,test1_object_points,test1_calibrate.camera_positions,test1_camera_matrix,test1_distortion_coef,folder_path1)
    test1_project_metashape.create_projections("metashape")


    ###############TEST 2: COMPARE CAMERA POSITIONS FROM OPENCV AND METASHAPE

    # 1: FIND CAMERA POSITIONS WITH CALIBRATECAMERA USING STILL IMAGES.
    # 2: FIND REPROJECTED PIXELS OF TARGETS WITH PROJECTPOINTS USING STILL IMAGES.
        # 2.1: USING CAMERA POSITIONS FROM METASHAPE.
        # 2.2: USING CAMERA POSITIONS FROM CALIBRATECAMERA.
    # 3: COMPARE (# 2) WITH ORIGINAL PIXELS OBTAINED FROM METASHAPE WITH FINDERRORS.

        # DATA USED:
        # camera positions= from still camera coordinates and CalibrateCamera.
        # object points = from still target coordinates.
        # camera matrix1 and dist. coeff.1 = from Metashape.
        # camera matrix2 and dist. coeff.2 = from CalibrateCamera.
        # images = from still images.

    print("START TEST 2\n")

    folder_path2='photos/still photos/'
    test2_object_points= lists.TARGET_S_COORDINATES
    test2_images= lists.STILL_IMAGE_PATHS
    test2_camera=lists.CAMERA_S_COORDINATES
    test2_camera_matrix=lists.CAMERA_MATRIX
    test2_distortion_coefs=lists.DISTORTION_COEF
    test2_pixels=lists.PIXELS_S_COORDINATES

    test2_calibrate=CalibrateCamera(test2_images,test2_object_points)
    test2_calibrate.set_pixels(test2_pixels)
    test2_calibrate.solve_pnp()

    #Comparing camera positions given by Opencv and Metashape: using camera matrix and dist. coefficients from Metashape
    test2_project_opencv=ProjectPoints(test2_images,test2_pixels,test2_object_points,test2_calibrate.camera_positions,test2_camera_matrix,test2_distortion_coefs,folder_path2)
    test2_project_opencv.create_projections("opencv")
    test2_project_metashape=ProjectPoints(test2_images,test2_pixels,test2_object_points,test2_camera,test2_camera_matrix,test2_distortion_coefs,folder_path2)
    test2_project_metashape.create_projections("metashape")

    #Comparing camera positions given by OpenCv and Metashape: using camera matrix and dist. coefficients from Test1 Opencv
    test2_project_opencv=ProjectPoints(test2_images,test2_pixels,test2_object_points,test2_calibrate.camera_positions,cam_matrix_opencv,d_coefficients_opencv,folder_path2)
    test2_project_opencv.create_projections("opencv")
    test2_project_metashape=ProjectPoints(test2_images,test2_pixels,test2_object_points,test2_camera,cam_matrix_opencv,d_coefficients_opencv,folder_path2)
    test2_project_metashape.create_projections("metashape")








#https://python.hotexamples.com/examples/cv2/-/projectPoints/python-projectpoints-function-examples.html

