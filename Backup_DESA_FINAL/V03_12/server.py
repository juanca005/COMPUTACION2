#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
from http.server import BaseHTTPRequestHandler
import io
import os
from flask import Flask, request, redirect, url_for, send_from_directory
import werkzeug 
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import numpy as np
import cv2
import time
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
import os
from librerias import *
import fotogramas
import algoritmo
import random
import string
from flask import send_from_directory
from flask import send_file



#print digits + chars


#char = "abcdefghijklmnñopqrstuvwyz"
#letra_aleatoria = random.choice(char)

#UPLOAD_FOLDER = 'dir/' + letra_aleatoria

ALLOWED_EXTENSIONS = set(['mov', 'avi', 'mkv','mp4'])

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#traigo de los otros modulos (es lo mismo de main.py)



def main(dir,filename):
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=fotogramas.dividir, args=(dir+'/'+filename,))
    p2 = multiprocessing.Process(target=algoritmo.compara, args=(dir+'/'+filename,q,))

    p.start()
    p.join()
    p2.start()
    #p2.join()
    #p.join()
    while True:
        if not q.empty():
            read = q.get()
            print(read)
            return url_for('uploaded_file',filename=filename)
    p2.join()
   
    
    #t1 = threading.Thread(name="h1", target=fotogramas.dividir, args=(dir+'/'+filename,))
    #t2 = threading.Thread(name="h2" , target=algoritmo.compara,args=(dir+'/'+filename,))
    
    #t1.start()
    
    #t1.join()
    #t2.start()
    #t2.join()





#fin de traer los otros modulos


def allowed_file(filename):
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
  
    return filename[-3:].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    char = "abcdefghijklmnñopqrstuvwyz"
    letra_aleatoria = random.choice(char)
    #print(letra_aleatoria)
    UPLOAD_FOLDER = 'dir/' + letra_aleatoria
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    a = logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print ('**archivo encontrado', file.filename)
            filename = secure_filename(file.filename)
            os.mkdir(UPLOAD_FOLDER)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main(UPLOAD_FOLDER,filename)
          
            #return url_for('uploaded_file',filename=filename)


        
    return '''
    <!doctype html>
    <title>Bird_Detection</title>
    <h1 style="text-align: center;"><span style="color: #339966;"><strong>BIRD DETECTION</strong></span></h1>
<p><strong><img style="display: block; margin-left: auto; margin-right: auto;" src="https://cdn.download.ams.birds.cornell.edu/api/v1/asset/251979231/" alt="" width="423" height="238" /><br /></strong></p>
<p>&nbsp;</p>
<form action="" enctype="multipart/form-data" method="post">
<p style="text-align: center;"><input name="file" type="file" /></p>
<p style="text-align: center;">&nbsp;</p>
<p style="text-align: center;"><input type="submit" value="PROCESAR VIDEO" /></p>
</form>
    '''
    
@app.route('/mov/dir/d/<filename>')
def uploaded_file(filename):
    
    
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)




if __name__ == '__main__':
    
    
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
    