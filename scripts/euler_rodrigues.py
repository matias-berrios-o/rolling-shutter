import numpy as np
import math as m
import cv2 as cv

def rot(d):
    x=m.radians(d[0])
    y=m.radians(d[1])
    z=m.radians(d[2])
    do=(x,y,z)
    '''Build a rotation matrix given a tuple of three angles (in radians) for rotations around x, y, and z.'''
    ox,oy,oz = do
    Rx = np.array([[1,0,0],[0,np.cos(ox),-np.sin(ox)],[0,np.sin(ox),np.cos(ox)]])
    Ry = np.array([[np.cos(oy),0,np.sin(oy)],[0,1,0],[-np.sin(oy),0,np.cos(oy)]])
    Rz = np.array([[np.cos(oz),-np.sin(oz),0],[np.sin(oz),np.cos(oz),0],[0,0,1]])
    R = np.dot(Rz,np.dot(Ry,Rx))

    v,jacobian=cv.Rodrigues(R)

    return v
    