
import cv2 as cv
from cv2 import imshow
import numpy as np
import create_lists as lists
from projection_finder import CalibrateCamera, ProjectPoints

if __name__ == '__main__':
    #FINAL: PROJECT POINTS USING 3D TARGETS COORDINATES TAKEN FROM STILL IMAGES AND 3D CAMERA COORDINATES TAKEN FROM MOVING IMAGES.
        #camera= from moving camera coordinates.
        #object_points= from still target coordinates.
        #camera_matrix= from still images.
    #print("START FINAL\n")
    #final_object_points= lists.TARGET_S_COORDINATES
    #final_images= lists.MOVING_IMAGE_PATHS
    #final_camera=lists.CAMERA_M_COORDINATES
    #final_camera_matrix=lists.CAMERA_MATRIX
    #final_distortion_coefs=lists.DISTORTION_COEF
    #final_projectpoints=ProjectPoints(final_images,final_object_points,final_camera,final_camera_matrix,final_distortion_coefs)
    #final_projectpoints.create_projections()
    #print("IMAGE POINTS FROM FINAL_PROJECTPOINTS:\n")
    #print(final_projectpoints.projection_pixels)
    #FINAL_REPROJECTION_PIX=final_projectpoints.projection_pixels
    

    #TEST:
    # 1: FINDING PIXELS OF TARGETS IN 12 CROPPED IMAGES WITH CALIBRATECAMERA.
    # 2: FINDING REPROJECTED PIXELS OF TARGETS WITH PROJECTPOINTS. 
    # 3: COMPARING 1 AND 2 WITH ORIGINAL PIXELS OBTAINED FROM METASHAPE.

        #camera=from still camera coordinates.
        #object_points= from still target coordinates.
        #camera_matrix= from still images.

    print("START TEST\n")
    test_object_points= lists.TARGET_S_COORDINATES
    test_images= lists.STILL_IMAGE_PATHS

  
    test_camera=lists.CAMERA_S_COORDINATES
    test_camera_matrix=lists.CAMERA_MATRIX
    test_distortion_coefs=lists.DISTORTION_COEF
    test_pixels=lists.PIXELS_S_COORDINATES

    #print(test_object_points)
    test_calibrate=CalibrateCamera(test_images,test_object_points,test_pixels)
    #test_calibrate.circles_grid_centers()
    #print(test_calibrate.object_points)

    print("\nIMAGE POINTS FROM TEST_CAMERA CALIBRATION:\n")
    print(test_calibrate.pixels)
    test_calibrate.calibrate()

    #TEST_CALIBRATION_PIX=test_calibrate.image_points
    #test_projectpoints=ProjectPoints(test_images,test_calibrate.image_points,test_object_points,test_camera,test_camera_matrix,test_distortion_coefs)
    #test_projectpoints.create_projections()
    #print("\nIMAGE POINTS FROM TEST_PROJECTPOINTS:\n")
    #test_images_paths=['DSC09901.JPG','DSC09902.JPG','DSC09905.JPG','DSC09906.JPG','DSC09908.JPG','DSC09909.JPG','DSC09910.JPG','DSC09911.JPG','DSC09912.JPG','DSC09913.JPG','DSC09914.JPG','DSC09939.JPG']
    #test_filter_reprojections=filter(test_projectpoints.projection_pixels,test_images_paths)
    #print(test_filter_reprojections)
    #TEST_REPROJECTION_PIX=test_filter_reprojections






    #final_calibrate=[]
    #for i in test_calibrate.image_points:
        #name=i[0].split("/")
        #image_name=name[2]
        #for j in i[1]:
            #new=[image_name,j[0][0],j[0][1]]
        #final_calibrate.append(new)

    #final_reproject=[]
    #for i in test_filter_reprojections:
        #image_name=i[0]
        #for j in i[1]:
            #new=[image_name,j[0][0],j[0][1]]
        #final_reproject.append(new)











#https://python.hotexamples.com/examples/cv2/-/projectPoints/python-projectpoints-function-examples.html

