#!/usr/bin/python3
# -*- coding: utf-8 -*-


from librerias import *



_lock = threading.RLock()
def _acquireLock():
   
    if _lock:
        _lock.acquire()

def _releaseLock():
    
    if _lock:
        _lock.release()



def log(ubicacion,prov):
    _acquireLock()
    try:

        #print("")
        fic = open("ubicacion.txt", "a")
    
        fic.write(ubicacion)
        fic.write("--------")
        fic.write(prov)
        fic.write("\n")
    
        fic.close()
    
    finally:
        _releaseLock()