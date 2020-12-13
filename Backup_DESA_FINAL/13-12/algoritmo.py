#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from librerias import *
import os
from cv2 import cv2

def compara(ruta, queue_1, queue_2):
    os.makedirs("mov/" + ruta)
    os.makedirs("static/imagenes/mov/"+ruta)
    path = 'cap/'+ruta
    original = cv2.imread(path+'/'+'0.jpg')
    for filename in os.listdir(path):
        image_to_compare = cv2.imread(os.path.join(path, filename))
        if original.shape == image_to_compare.shape:
            print('Las imagenes tiene el mismo tamaño y canal')
            difference = cv2.subtract(original, image_to_compare)
            canal_blue, canal_green, canal_red = cv2.split(difference)
            print(cv2.countNonZero(canal_blue))
        if (cv2.countNonZero(canal_blue) == 0 and cv2.countNonZero(canal_green) == 0 and cv2.countNonZero(canal_red) == 0):
            print('Las imagenes son completamente iguales')
        else:
            print('Las imagenes no son iguales')
            shift = cv2.xfeatures2d.SIFT_create()
            kp_1, desc_1 = shift.detectAndCompute(original, None)
            kp_2, desc_2 = shift.detectAndCompute(image_to_compare, None)
            print("Keypoints 1st image", str(len(kp_1)))
            print("Keypoints 2st image", str(len(kp_2)))
            index_params = dict(algorithm=0, trees=5)
            search_params = dict()
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(desc_1, desc_2, k=2)
            good_points = []
            for var_m, var_n in matches:
                if var_m.distance < 0.6*var_n.distance:
                    good_points.append(var_m)
            number_keypoints = 0
            if len(kp_1) <= len(kp_2):
                number_keypoints = len(kp_1)
            else:
                number_keypoints = len(kp_2)
            print("GOOD matches", len(good_points))
            print("Que tan bueno es el match", len(good_points) / number_keypoints * 100, "%")
            if len(good_points) / number_keypoints * 100 < 99:#valor de siempre 77
                path2 = "mov/"+ruta
                path3 = "static/imagenes/mov/"+ruta
                #path_final = os.path.join(path3 , str(filename))
                #print("path final",path_final)
                print("deberiamos registrar movimiento")
                cv2.imwrite(os.path.join(path2, str(filename)), image_to_compare)
                cv2.imwrite(os.path.join(path3, str(filename)), image_to_compare)
                queue_1.put(filename)#quiero devolver las imagenes con movimiento al proceso padre
                queue_2.put(path3)
            else:
                print("no debemos registrar mov")
                cv2.drawMatches(original, kp_1, image_to_compare, kp_2, good_points, None)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
