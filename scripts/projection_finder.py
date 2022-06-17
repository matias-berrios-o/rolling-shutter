import cv2 as cv
from cv2 import imshow
import numpy as np
import create_lists as lists



#CALIBRATE CAMERA, need more data
class CalibrateCamera: 
    def __init__(self,images,object_points):

        self.image_points=[]
        self.object_points=np.array(object_points)#list of coordinates
        self.dist_coeff=[0]
        self.images=images #list of images
        self.boardSize=(7,5)
        #define columns and rows
        self.criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        #define criteria


    def circles_grid_centers(self):

        #To consider: The parameters below depend on pixel distances, areas, etc. The images have to be similar to be able to use the same parameters. For different sets of images, different parameters are needed.
        #For example: from folder "cropped_images" images sets are DSC09900 to DSC09915, DSC9916 to DSC09926, DSC09927 to DSC09934, etc.
        #FROM CROPPED_IMAGES, 12 SUCCESSFUL CIRCLESGRID DETECTION FOR 35 CIRCLES.
        blobParams = cv.SimpleBlobDetector_Params()
        blobParams.filterByCircularity = True
        blobParams.minCircularity = 0.2
        blobParams.minDistBetweenBlobs = 130
        blobParams.filterByInertia = True
        blobParams.minInertiaRatio = 0.01
        blobParams.filterByArea = True
        blobParams.minArea = 1100
        blobParams.maxArea = 1800
        blobParams.minThreshold = 8.5
        blobParams.maxThreshold = 2000
        blobParams.filterByColor = True
        blobParams.blobColor=0

        self.blobdetector = cv.SimpleBlobDetector_create(blobParams)


        for image in self.images:
            img=cv.imread(image)
            self.gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
            keypoints = self.blobdetector.detect(self.gray)
            self.im_with_keypoints = cv.drawKeypoints(self.gray, keypoints, np.array([]), (0,255,0), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            #cv.imshow('img',self.im_with_keypoints)
            #cv.waitKey(0)
            im_with_keypoints_gray = cv.cvtColor(self.im_with_keypoints, cv.COLOR_BGR2GRAY)
            self.retval,self.centers=cv.findCirclesGrid(self.im_with_keypoints, self.boardSize, flags=(cv.CALIB_CB_SYMMETRIC_GRID+cv.CALIB_CB_CLUSTERING),blobDetector=self.blobdetector,parameters=None)
            if self.retval == True: 
              #cornerSubPix(image, corners, winSize, zeroZone, criteria) -> corners
                self.centers2=cv.cornerSubPix(self.gray, self.centers, (11,11),(-1,-1), self.criteria) 

                self.image_points.append([image,self.centers2])
    
 
        # Draw and display the corners

                img = cv.drawChessboardCorners(img, self.boardSize, self.centers2, self.retval)



                #cv.imshow('img',img)
                #cv.waitKey(0)

    


#CANNOT FIGURE OUT OBJECT POINTS AND IMAGE POINTS TYPE TO MAKE IT WORK :(
    def calibrate(self):
        #what is gray????? should this be for each picture???
        self.retval_2,self.cam_matrix,self.dist_coeff,self.rotation_vector,self.translation_vector=cv.calibrateCamera(self.object_points, self.image_points, self.gray.shape[::-1], None, None)
       # img = cv.imread('newimage') #what do i put in here?
       # h,  w = img.shape[:2]
        print(self.retval_2)
        print(self.cam_matrix)
        print(self.dist_coeff)
        print(self.rotation_vector)
        print(self.translation_vector)
       # self.newcam_mtx, roi=cv.getOptimalNewCameraMatrix(self.cam_matrix,self.dist_coeff,(w,h),1,(w,h))


class ProjectPoints:

    def __init__(self, images, obj_coordinates_3d, camera_coordinates_3d, cam_matrix,dist_coef):

        self.obj_coordinates=np.array(obj_coordinates_3d)
        self.images=images
        self.camera_coordinates=camera_coordinates_3d
        self.camera_matrix=cam_matrix
        self.distortion_coef=dist_coef
        self.projection_pixels=[]


    def projections(self,filename,rotation_vector,translation_vector):
        print(type(rotation_vector))
        print(translation_vector)

        pixels=cv.projectPoints(self.obj_coordinates,rotation_vector,translation_vector,self.camera_matrix,self.distortion_coef)
        blank_image = np.zeros((4000,4000,3), np.uint8)

        for pixel in pixels[0]:
            print(pixel[0][0])
            print(type(pixel[0][0]))
            blank_image=cv.circle(blank_image,(int(pixel[0][0]),int(pixel[0][1])), radius=5,color=(255,0,0),thickness=-1)
    
        imshow("reprojection",blank_image)
        cv.waitKey(0)

        self.projection_pixels.append([filename,pixels[0]])



    def create_projections(self):

        for camera in self.camera_coordinates:
            filename=camera[0]   
            translation_vector=np.array(camera[1])
            rotation_vector=np.array(camera[2])

            self.projections(filename,rotation_vector,translation_vector)
        

class FindErrors:
    def __init__(self,pixels_AM,pixels_P):
       #RAW LISTS DIRECTLY FROM PROJECTPOINTS AND AGISOFTMETASHAPE
        self.coordinates_AM=pixels_AM
        self.coordinates_P=pixels_P
        self.coordinates_CC=[]

        #FILTERED LISTS WITH ACCESSIBLE PIXELS
        self.coordinates_AM_filter=self.filter_AM()
        self.coordinates_P_filter=self.filter_P()
        self.coordinates_CC_filter=self.filter_CC()

    #RAW LIST DIRECTLY FROM CALIBRATECAMERA
    def add_coordinates_CC(self, pixels_BD):
        self.coordinates_CC=pixels_BD

    def filter_AM(self):

        pass
    
    def filter_P(self):
        pass

    def filter_CC(self):
        new=[]
        for i in range(len(self.coordinates_CC)):
            for j in range(len(i[1])):
                target_name='target '+str(j)
                target_x=i[1][0][j][0]
                target_y=i[1][0][j][1]
                pixel_coord=[i[0],target_name,target_x,target_y]
                new.append(pixel_coord)
        return new
                

def filter(points, image_names):
    new=[]
    for i in range(len(points)):
        for  j in range(len(image_names)):
            if points[i][0]==image_names[j]:
                new.append(points[i])
    return new

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
    test_images= lists.CROPPED_IMAGE_PATHS
    test_camera=lists.CAMERA_S_COORDINATES
    test_camera_matrix=lists.CAMERA_MATRIX
    test_distortion_coefs=lists.DISTORTION_COEF

    test_calibrate=CalibrateCamera(test_images,test_object_points)
    test_calibrate.circles_grid_centers()
    print("IMAGE POINTS FROM TEST_CAMERACALIBRATION:\n")
    #print(test_calibrate.image_points)
    #print("\n")
    TEST_CALIBRATION_PIX=test_calibrate.image_points
    test_projectpoints=ProjectPoints(test_images,test_object_points,test_camera,test_camera_matrix,test_distortion_coefs)
    test_projectpoints.create_projections()
    print("IMAGE POINTS FROM TEST_PROJECTPOINTS:\n")
    #print(projectpoints.projection_pixels)
    test_images_paths=['DSC09901.JPG','DSC09902.JPG','DSC09905.JPG','DSC09906.JPG','DSC09908.JPG','DSC09909.JPG','DSC09910.JPG','DSC09911.JPG','DSC09912.JPG','DSC09913.JPG','DSC09914.JPG','DSC09939.JPG']
    test_filter_reprojections=filter(test_projectpoints.projection_pixels,test_images_paths)
    #print(test_filter_reprojections)
    TEST_REPROJECTION_PIX=test_filter_reprojections

    test_projection_metashape=lists.PIXELS_S_COORDINATES






    final_calibrate=[]
    for i in test_calibrate.image_points:
        name=i[0].split("/")
        image_name=name[2]
        for j in i[1]:
            new=[image_name,j[0][0],j[0][1]]
        final_calibrate.append(new)

    final_reproject=[]
    for i in test_filter_reprojections:
        image_name=i[0]
        for j in i[1]:
            new=[image_name,j[0][0],j[0][1]]
        final_reproject.append(new)











#https://python.hotexamples.com/examples/cv2/-/projectPoints/python-projectpoints-function-examples.html

