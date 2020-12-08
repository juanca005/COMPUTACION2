#!/usr/bin/python3
# -*- coding: utf-8 -*-

from librerias import *




def compara(ruta,q):
       os.makedirs("mov/"+ruta)
       path='cap/'+ruta

       #data = []
       #image_names = []

       original = cv2.imread(path+'/'+'0.jpg')

       for filename in os.listdir(path):
              
              image_to_compare = cv2.imread(os.path.join(path,filename))
              if original.shape == image_to_compare.shape:
                  print('Las imagenes tiene el mismo tamaño y canal')
                  difference = cv2.subtract(original, image_to_compare)
                  b, g, r = cv2.split(difference)
                  print(cv2.countNonZero(b))
              if (cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0):
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
              for m, n in matches:
                  if m.distance < 0.6*n.distance:
                      good_points.append(m)

              number_keypoints = 0
              if (len(kp_1) <= len(kp_2)):
                
                  number_keypoints = len(kp_1)
              else:
                  number_keypoints = len(kp_2)

              print("GOOD matches",len(good_points))
              print("Que tan bueno es el match", len(good_points) / number_keypoints * 100, "%")

              if(len(good_points) / number_keypoints * 100 < 77):
                  path2="mov/"+ruta
                  print("deberiamos registrar movimiento")
                  cv2.imwrite(os.path.join(path2 , str(filename)),image_to_compare)
               
                  q.put(filename)  #quiero devolver las imagenes con movimiento al proceso padre
                  
                  """  folder = 'cap'
                  for the_file in os.listdir(folder):
                      file_path = os.path.join(folder, the_file)
                      try:
                          if (os.path.isfile(file_path) and file_path != "cap/0.jpg"):
                              os.unlink(file_path)
                      except Exception as e:
                          print(e) """

                  
              else:
                  print("no debemos registrar mov")
              result = cv2.drawMatches(original, kp_1, image_to_compare, kp_2, good_points, None)
              #return path2

              cv2.waitKey(0)
              cv2.destroyAllWindows()
   
        