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



def log(hilo,prov,ip,time):
    _acquireLock()
    try:

        #print("")
        fic = open("ubicacion.txt", "a")

        fic.write("---Hilo--->")
        fic.write(hilo)
        fic.write("---Ubicacion cliente--->")
        fic.write(prov)
        fic.write("---Direccion Ip del cliente--->")
        fic.write(ip)
        fic.write("---Fecha/hora de conexión--->")
        fic.write(str(time))
        fic.write("\n")
    
        fic.close()
    
    finally:
        _releaseLock()