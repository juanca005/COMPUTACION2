#!/usr/bin/python3
# -*- coding: utf-8 -*-


from librerias import *






def muestra(q,q2):
    while True:
        ubi=q2.get()
        if not q.empty():

            
            #print("rutaaaa",ubi)
            read = q.get()
            #print("desde el proceso muestra",read)
            
            image_path= (ubi +'/'+read)
            #print("image_path",image_path)
            
            
            #img = cv2.imread(image_path)
            #home(image_path) 
            #window_width=800 
            #window_height=600

           
            #cv2.namedWindow("BIRD DETECTION", cv2.WINDOW_NORMAL)

            
            #cv2.resizeWindow("BIRD DETECTION", window_width, window_height)

            

            #cv2.imshow("BIRD DETECTION",img) 

            
            #cv2.waitKey(0) 

            #home()

        #cv2.destroyAllWindows() 


       