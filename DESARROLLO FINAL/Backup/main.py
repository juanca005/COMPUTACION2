#!/usr/bin/python3
# -*- coding: utf-8 -*-

import fotogramas
import algoritmo
from librerias import *

if __name__ == '__main__':
    t1 = threading.Thread(name="h1", target=fotogramas.dividir, args=("dir/aa.mp4",))
    t2 = threading.Thread(name="h2" , target=algoritmo.compara,args=())
    t1.start()
    
    t1.join()
    t2.start()
    t2.join()

    
    #print(t1.is_alive())
       
    #fotogramas.dividir("videos/aa.mp4")
    #algoritmo.compara()
