
import cv2 as cv
import numpy as np



PATH_1="scripts/files/camera_m_xyz_ang.txt"
PATH_2="scripts/files/target_m_xyz.txt"
PATH_3="scripts/files/camera_s_xyz_ang.txt"
PATH_4="scripts/files/target_s_xyz.txt"
PATH_5="scripts/files/pixels_m.txt"
PATH_6="scripts/files/pixels_s.txt"
PATH_MATRIX="scripts/files/matrix.txt"

PATH_7="photos/cropped_images"

#FOR ANY TXT FILE
#RECEIVES FILE PATH AND READS INFORMATION, CREATES LIST OF LISTS WITH INFORMATION
#OUTPUT: UNFILTERED LIST OF LISTS
def open_files(type,path):
    data_file=[]
    if type!="pixel":
        with open(path, 'r') as file:
            file_information=file.readlines()
            for line in file_information:
                line=line.strip()
                line=line.split(",")
                data_file.append(line)

    else:
        with open(path, 'r') as file:
            file_information=file.readlines()
            for line in file_information:
                line=line.strip()
                line=line.split("\t")
                data_file.append(line)

    return data_file

#FOR ANY FILE
#SEPARATES TITLES AND EXTRA INFORMATION CONTAINED IN FILE, CREATES LIST OF LISTS WITH TARGET NAME AND INFORMATION FROM FILE INFORMATION.
#OUTPUT: FILTERED LIST OF LISTS [["target 1",float(x1),float(y1),float(z1)],["target 2",float(x2),float(y2),float(z2)],....["target n",float(xn),float(yn),float(zn)]]
def filter_information(type,data_files):
    data_=[]
    if type!="pixel":
        for line in data_files[2:]:
            new_line=[]
            for i in line:
                if i!="":
                    new_line.append(i)
            data_.append(new_line)
    else:
        for line in data_files[1:]:
            new_line=[line[0],"target "+str(line[1]),line[2],line[3]]
            data_.append(new_line)

    return data_

#ONLY FOR TARGETS FROM 'STILL' FILES
#CREATES LIST OF LISTS WITH TARGET NAME AND CORRESPONDING COORDINATES. FILTERS INFORMATION FROM REFERENCE TARGETS
#CONSIDERATION: TARGETS THAT WERE USED AS REFERENCES MUST BE FILTERED TO GET CORRESPONDING COORDINATES
#OUTPUT: FILTERED LIST OF LISTS [["target 1",float(x1),float(y1),float(z1)],["target 2",float(x2),float(y2),float(z2)],....["target n",float(xn),float(yn),float(zn)]]
def targets_xyz_still(data_targets):
    xy_estimates=[]
    for target in data_targets:
        if target[0]=='target 8' or target[0]=='target 51' or target[0]=='target 159' or target[0]=='target 59' :
            new_target=[target[0],float(target[9]),float(target[10]),float(target[11])]
            xy_estimates.append(new_target)

        else:
            target[1]=float(target[1])
            target[2]=float(target[2])
            target[3]=float(target[3])
            xy_estimates.append(target)
    return xy_estimates[:len(data_targets)-1]

#ONLY FOR TARGETS FROM 'MOVING' FILES
#CREATES LIST OF LISTS WITH TARGET NAME AND CORRESPONDING COORDINATES. FILTERS INFORMATION FROM REFERENCE TARGETS
#CONSIDERATION: TARGETS THAT WERE USED AS REFERENCES MUST BE FILTERED TO GET CORRESPONDING COORDINATES
#OUTPUT: FILTERED LIST OF LISTS [["target 1",float(x1),float(y1),float(z1)],["target 2",float(x2),float(y2),float(z2)],....["target n",float(xn),float(yn),float(zn)]]
def targets_xyz_moving(data_targets):
    xy_estimates=[]
    for target in data_targets:
        if target[0]=='target 8' or target[0]=='target 5' or target[0]=='target 4' or target[0]=='target 51' :
            new_target=[target[0],float(target[9]),float(target[10]),float(target[11])]
            xy_estimates.append(new_target)

        else:
            target[1]=float(target[1])
            target[2]=float(target[2])
            target[3]=float(target[3])
            xy_estimates.append(target)
    return xy_estimates[:len(data_targets)-1]

#ONLY FOR TARGET FILES
#RECEIVES A LIST OF LISTS OF TARGET COORDINATES WITH TARGET NAME, ELIMINATES THE TARGET NAME TO ONLY LEAVE THE TARGET COORDINATES
#OUTPUT: LIST OF TUPLES [(float(x1),float(y1),float(z1)),(float(x2),float(y2),float(z2)),....(float(xn),float(yn),float(zn))]
def only_coordinates(data):
    final_coordinates=[]

    for line in data:
        coordinates=(float(line[1]),float(line[2]),float(line[3]))
        final_coordinates.append(coordinates)

    return np.array(final_coordinates,dtype=np.float32)

#ONLY FOR CAMERA FILES
#FILTERS CAMERA DATA OBTAINED FROM CAMERA FILES TO OBTAIN FILENAME, XYZ COORDINATES AND YAW PITCH ROLL COORDINATES
#OUTPUT: LIST OF LISTS WITH TUPLES FOR ROTATION AND TRANSLATION VECTORS [["FILEPATH1",(float(x1),float(y1),float(z1)),(float(yaw1),float(pitch1),float(roll1))],....["FILEPATHn",(float(xn),float(yn),float(zn)),(float(yawn),float(pitchn),float(rolln))]]
def camera_coordinates(data):
    final_coordinates=[]

    for line in data:
        x=float(line[1])
        y=float(line[2])*-1
        z=float(line[3])
        yaw=float(line[4])
        pitch=float(line[5])
        roll=float(line[6])
        coordinates=[line[0],[x,y,z],[yaw,pitch,roll]]
        final_coordinates.append(coordinates)
    return final_coordinates

#ONLY FOR PIXEL FILES
#FILTERS PIXEL DATA OBTAINED FROM PIXEL FILES TO OBTAIN FILENAME, TARGET NAME, X, Y
#OUTPUT: LIST OF LISTS LIST OF LISTS [["FILEPATH1","target 1",float(x1),float(y1)],["FILEPATH1","target 2",float(x2),float(y2)],....["FILEPATHn","target n",float(xn),float(yn)]]
def pixel_coordinate(data):
    final_coordinates=[]
    
    for line in data:
        coordinates=[line[0],line[1],(float(line[2]),float(line[3]))]
        final_coordinates.append(coordinates)

    
    return final_coordinates

#ONLY FOR CAMERA FILES
#CREATES LIST WITH IMAGE PATHS, IMAGES PATHS ARE FOUND IN THE LIST CONTAINING CAMERA COORDINATES
#OUTPUT: LIST OF FILEPATHS ["FOLDER/FILEPATH1","FOLDER/FILEPATH2",..."FOLDER/FILEPATHn"]
def image_paths(folder,data):
    paths=[]
    for line in data:
        filepath=folder+"/"+line[0]
        paths.append(filepath)
    return paths

#ONLY FOR TARGET AND PIXEL FILES
#FILTERS A COORDINATE LIST FOR TARGETS I WANT TO USE, GIVEN BY LIST "BOARD_TARGETS". "BOARD_TARGETS" IS SORTED TO BE IN ORDER BY TARGET NUMBER.
#OUTPUT: LIST OF LISTS [["target 1",float(x1),float(y1),float(z1)],["target 2",float(x2),float(y2),float(z2)],....["target n",float(xn),float(yn),float(zn)]]
def filter_points(type,data,board_targets):
    new_board_coordinates=[]
    if type!="pixel":

        for dat in data:
            for target in board_targets:
                if dat[0]==target:
                    new_board_coordinates.append(dat)

    else:
        for dat in data:
            for target in board_targets:
                if dat[1]==target:
                    new_board_coordinates.append(dat)

    return new_board_coordinates


def np_array_pixels(data):
    img_paths=[]

    for dat in data:
        if dat[0] not in img_paths:
            img_paths.append(dat[0])

    final=[]
    for img in img_paths:
        pixels=[]
        for dat in data:
            if img==dat[0]:
                pixels.append(dat[2])
        pixels=np.array(pixels,dtype=np.float32)
        final.append([img,pixels])
    
    return final
    
##TARGETS TO USE:
#Row 1 : 3 66 6 53 9 63 13
#Row 2 : 50 157 60 159 57 161 55
#Row 3 : 2 49 5 51 8 65 12
#Row 4 : 56 160 52 158 64 145 61
#Row 5 : 1 58 4 59 7 54 11

board_targets=["target 3","target 66","target 6","target 53","target 9","target 63","target 13",
"target 50","target 157","target 60","target 159","target 57","target 161","target 55",
"target 2","target 49","target 5","target 51","target 8","target 65","target 12",
"target 56","target 160","target 52","target 158","target 64","target 145","target 61",
"target 1","target 58","target 4","target 59","target 7","target 54","target 11"]

board_targets.sort(key=lambda x: int(x[7:len(x)]))



####PRUEBA

###GET TARGET DATA

#PATH 4: TARGET_S
type_="target"
s4=open_files(type_,PATH_4)

target_s_filter1=filter_information(type_,s4)

target_s_filter2=targets_xyz_still(target_s_filter1)

#target_s_boardfilter=filter_points(type_,target_s_filter2,board_targets)

target_s_xyz=only_coordinates(target_s_filter2)
#print(target_s_xyz)


#PATH 2: TARGET_M
type_="target"
s2=open_files(type_,PATH_2)

target_m_filter1=filter_information(type_,s2)

target_m_filter2=targets_xyz_moving(target_m_filter1)

#target_m_boardfilter=filter_points(type_,target_m_filter2,board_targets)

target_m_xyz=only_coordinates(target_m_filter2)

###GET CAMERA DATA

#PATH 1: CAMERA_M
type_="camera"
s1=open_files(type_,PATH_1)

camera_m_filter1=filter_information(type_,s1)

camera_m_xyz=camera_coordinates(camera_m_filter1)

m_image_paths=image_paths("photos/moving photos",camera_m_xyz)


#PATH 3: CAMERA_S
type_="camera"
s3=open_files(type_,PATH_3)
matrix=open_files(type_,PATH_MATRIX)

camera_s_filter1=filter_information(type_,s3)

camera_s_xyz=camera_coordinates(camera_s_filter1)

s_image_paths=image_paths("photos/still photos",camera_s_xyz)

cropped_image_paths=image_paths(PATH_7,camera_s_xyz)

###GET PIXEL DATA

#PATH 5: PIXELS_M
type_="pixel"
s5=open_files(type_,PATH_5)

pixels_m_filter1=filter_information(type_,s5)

pixels_m_xyz=pixel_coordinate(pixels_m_filter1)

pixels_m_array=np_array_pixels(pixels_m_xyz)

#pixels_m_boardfilter=filter_points(type_,pixels_m_xyz,board_targets)


#PATH 6: PIXELS_S
type_="pixel"
s6=open_files(type_,PATH_6)

pixels_s_filter1=filter_information(type_,s6)

pixels_s_xyz=pixel_coordinate(pixels_s_filter1)

pixels_s_array=np_array_pixels(pixels_s_xyz)

print(pixels_s_array)

#pixels_s_boardfilter=filter_points(type_,pixels_s_xyz,board_targets)



####VARIABLES FOR EXPORTING

#Targets used are given by and sorted in the same order as 'board_targets'.
#Target coordinates are given in X,Y,Z order. List of tuples.
#Cameras are given in FILENAME,X,Y,Z,YAW,PITCH,ROLL. List of lists.
#pixels are given in FILENAME,TARGET NAME,X,Y order. List of lists.

TARGET_S_COORDINATES=target_s_xyz
TARGET_M_COORDINATES=target_s_xyz

CAMERA_S_COORDINATES=camera_s_xyz
CAMERA_M_COORDINATES=camera_m_xyz

STILL_IMAGE_PATHS=s_image_paths
MOVING_IMAGE_PATHS=m_image_paths
CROPPED_IMAGE_PATHS=cropped_image_paths

PIXELS_S_COORDINATES=pixels_s_array
PIXELS_M_COORDINATES=pixels_m_array

#OPEN CAMERA CALIBRATION XML FILE

cv_file=cv.FileStorage("scripts/opencv_cam_calibration.xml",cv.FILE_STORAGE_READ)

CAMERA_MATRIX=cv_file.getNode("Camera_Matrix").mat()
DISTORTION_COEF=cv_file.getNode("Distortion_Coefficients").mat()
print("read camera matrix\n",CAMERA_MATRIX)
print("read distortion matrix\n",DISTORTION_COEF)

cv_file.release()
