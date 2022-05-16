
from cmath import sqrt
from re import A
import numpy as np

PATH_1="moving_cameras_xys_est.txt"
PATH_2="moving_targets_xyz_est.txt"
PATH_3="still_cameras_xyz_est.txt"
PATH_4="still_target_xyz_est.txt"


def abrir_archivos(path):
    datos_archivo=[]
    with open(path, 'r') as archivo:
        lista_coordenadas=archivo.readlines()
        for line in lista_coordenadas:
            line=line.strip()
            line=line.split(",")
            datos_archivo.append(line)
    return datos_archivo


#recibe resultado de funcion abrir_archivos
def separar_titulos(datos_archivo):
    datos_targets=[]
    for line in datos_archivo[2:]:
        new_line=[]
        for i in line:
            if i!="":
                new_line.append(i)
        datos_targets.append(new_line)
    return datos_targets

#recibe resultado de funcion separar_titulos
def targets_referencia(datos_targets):
    referencias=[]
    #targets usados como puntos de referencia son 51, 8, 158
    for target in datos_targets:
        if target[0]=='target 8' or target[0]=='target 51' or target[0]=='target 158':
            referencias.append(target)
    return referencias

def total_error(datos_targets):
    errors=datos_targets[len(datos_targets)-1]
    return errors

#recibe resultado de funcion separar_titulos
def targets_xy_estimates_still(datos_targets):
    xy_estimates=[]
    for target in datos_targets:
        if target[0]=='target 8' or target[0]=='target 51' or target[0]=='target 159' or target[0]=='target 59' :
            new_target=[target[0],float(target[8]),float(target[9]),float(target[10])]
            xy_estimates.append(new_target)

        else:
            target[1]=float(target[1])
            target[2]=float(target[2])
            target[3]=float(target[3])
            xy_estimates.append(target)
    return xy_estimates[:len(datos_targets)-2]

def targets_xy_estimates_moving(datos_targets):
    xy_estimates=[]
    for target in datos_targets:
        if target[0]=='target 8' or target[0]=='target 5' or target[0]=='target 4' or target[0]=='target 51' :
            new_target=[target[0],float(target[8]),float(target[9]),float(target[10])]
            xy_estimates.append(new_target)

        else:
            target[1]=float(target[1])
            target[2]=float(target[2])
            target[3]=float(target[3])
            xy_estimates.append(target)
    return xy_estimates[:len(datos_targets)-2]

#recibe resultado de funcion targets_xy_estimates
def only_coordinates(datos):
    final_coordinates=[]

    for line in datos:
        coordinates=[float(line[1]),float(line[2]),float(line[3])]
        final_coordinates.append(coordinates)

    return final_coordinates





###PRUEBA


#PATH 4 still targets
s=abrir_archivos(PATH_4)
s=separar_titulos(s)
print(s)
still_targets_estimates=targets_xy_estimates_still(s)
print(still_targets_estimates)
still_targets_xyz=only_coordinates(still_targets_estimates)
print(still_targets_xyz)



#PATH 2 moving targets
s=abrir_archivos(PATH_2)
s=separar_titulos(s)
print(s)
moving_targets_estimates=targets_xy_estimates_moving(s)
print(moving_targets_estimates)
moving_targets_xyz=only_coordinates(moving_targets_estimates)
print(moving_targets_xyz)


#PATH 1 moving cameras
s=abrir_archivos(PATH_1)
moving_cameras_estimates=separar_titulos(s)
print(moving_cameras_estimates)
moving_cameras_xyz=only_coordinates(moving_cameras_estimates)
print(moving_cameras_xyz)


#PATH 3 still cameras
s=abrir_archivos(PATH_3)
still_cameras_estimates=separar_titulos(s)
print(still_cameras_estimates)
still_cameras_xyz=only_coordinates(still_cameras_estimates)
print(still_cameras_xyz)