#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from cv2 import cv2
from PIL import Image


def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)

def unir(upload_folder, image_path, filename):
    path_final = os.path.join(image_path, upload_folder, filename)
    print(path_final)
    pics = os.listdir(path_final)
    arreglo = []
    longitud_arreglo = len(arreglo)
    filename_final = 'final.jpg'
    filename_base = 'base.jpg'
    dst = Image.new('RGB', (1920, 1080))
    rutita = os.path.join(path_final, str(filename_base))
    rutita2 = os.path.join(path_final, str(filename_final))
    dst.save(rutita)
    #cv2.imwrite(os.path.join(path_final, str(filename_final)), dst)
    for pic in pics:
        arreglo.append(pic)
    longitud_arreglo = len(arreglo)  #deberia valer la cantidad de fotogramas
    #dst2 = cv2.imread(os.path.join(path_final, str(filename_base)))
    arreglo2 = []
    for i in range(longitud_arreglo):
        imagen1 = cv2.imread(os.path.join(path_final, arreglo[i]))
        arreglo2.append(imagen1)
        im_v_resize = vconcat_resize_min(arreglo2)
    cv2.imwrite(rutita2, im_v_resize)
