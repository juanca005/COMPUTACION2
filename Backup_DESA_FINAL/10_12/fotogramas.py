#!/usr/bin/python3
# -*- coding: utf-8 -*-

from librerias import *





def dividir(ruta):
       
       video_path = ruta
       print(ruta)
       os.makedirs("cap/"+ruta)

       path='cap/'+ruta
       cap = cv2.VideoCapture(video_path)
       length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
       print("cantidad de fotogramas" , length)
       
       img_index = 0
       i=0
       while (cap.isOpened()):
              ret, frame = cap.read()
              
              
              if ret == False:
                     break
              
              a = cv2.imwrite(os.path.join(path , str(img_index) + '.jpg'),frame)
              
              img_index += 1
              
       cap.release()
       cv2.destroyAllWindows()
