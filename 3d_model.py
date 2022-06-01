import cv2 as cv
from cv2 import calibrateCamera
import matplotlib.pyplot as plt

from create_lists import still_targets_xyz,moving_targets_xyz,moving_cameras_xyz,still_cameras_xyz


#CALIBRATE CAMERA, need more data
class CalibrateCamera:
    def __init__(self,images,object_points,image_points):

        self.images_points=image_points
        self.object_points=object_points
        self.cam_matrix,self.rotation_vector,self.translation_vector=cv.calibrateCamera()
        self.dist_coeff=[0]
        self.images=images

#K=intrinsic matrix or camera matrix:
    #[[fx,y,cx],[0,fy,cy],[0,0,1]]
    #fx,y= focal lengths
    #cx,y=coordinates of optical center in image plane
    #y=skew between axes

#extrinsic matrix:
    #rotation_vector= 3x3 matrix
    #translation_vector=3x1 matrix

class ProjectPoints:

    def __init__(self, obj_coordinates_3d, camera_coordinates_3d, object_points,image_points,image):

#define coordinates 3D
#obj_coordinates_still=still_targets_xyz
#obj_coordinates_moving=moving_targets_xyz

#camera_coordinates_still=still_cameras_xyz
#camera_coordinates_moving=moving_cameras_xyz
        self.obj_coordinates_3d=obj_coordinates_3d
        self.camera_coordinates_3d=camera_coordinates_3d
        self.camera=CalibrateCamera(image,object_points,image_points)
        self.projection_pixels_list=[]
        self.corrected_projection_pixels=[]
#from self.camera we get:
    #rotation_vector=[]
    #translation_vector=[]

    def create_2d_projection(self):
#find coordinates 2D
    #i want to use the still target coordinates since they should be the most accurate and the position of the moving cameras.
        for obj_coord in self.obj_coordinates_3d:


            self.projection_pixels=cv.projectPoints(obj_coord,self.camera.rotation_vector,self.camera.translation_vector,self.camera.cam_matrix,self.camera.dist_coeff)
            self.projection_pixels_list.append(self.projection_pixels)


    def projection_correction(self):
        pass

if __name__ == '__main__':
    #with still targets 3D coordinates
    #and moving cameras 3D coordinates

    #object_points=""
    #image_points=""
    #images=""
    points=ProjectPoints(still_targets_xyz,moving_cameras_xyz,object_points,image_points,images)
    print(points.corrected_projection_pixels)


##how do i define where the camera is??????
#https://python.hotexamples.com/examples/cv2/-/projectPoints/python-projectpoints-function-examples.html
##https://github.com/radjkarl/imgProcessor/blob/master/imgProcessor/camera/PerspectiveCorrection.py