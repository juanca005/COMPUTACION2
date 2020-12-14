#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime as dt
import logging
import threading
import os, shutil
import multiprocessing
from multiprocessing import Process, Queue
import random
from werkzeug.utils import secure_filename
from flask import Flask, flash, redirect, render_template, request, session, abort, send_file, send_from_directory, url_for
import fotogramas
import algoritmo
import log
import final

import numpy as np
from cv2 import cv2


ALLOWED_EXTENSIONS = set(['mov', 'avi', 'mkv', 'mp4'])

APLIC_BIRD = Flask(__name__)

def main(dir, filename):
    queue_1 = multiprocessing.Queue()
    queue_2 = multiprocessing.Queue()
    proc_1 = multiprocessing.Process(target=fotogramas.dividir, args=(dir+'/'+filename, ))
    proc_2 = multiprocessing.Process(target=algoritmo.compara, args=(dir+'/'+filename, queue_1, queue_2,))
    #proc_3 = multiprocessing.Process(target=final.unir, args=(queue_1, queue_2,))
    proc_1.start()
    proc_1.join()
    proc_2.start()
    #proc_3.start()
    proc_2.join()

    
            

    
    




    #ruta = queue_2.get()   #en ruta tengo la direccion completa para poder mostrar fotogramas pero no logro llevar a la funcion imagenes
    #print ("rutaaaaaaaaaaaaaaa colaaa",ruta)

@APLIC_BIRD.route('/<image_path>/<upload_folder>/<filename>/final.jpg')
def imagenes(upload_folder,image_path,filename):
    print(upload_folder)
    image_path = "static/imagenes/mov/dir"
    image_path2 = "g/video_corto.mp4"
    path_final = os.path.join(image_path, image_path2)
    pics = os.listdir(path_final)
    return render_template("mostrar.html", ruta=path_final, pics=pics)


def allowed_file(filename):
    return filename[-3:].lower() in ALLOWED_EXTENSIONS

@APLIC_BIRD.route('/', methods=['GET', 'POST'])
def upload_file():
    char = "abcdefghijklmnñopqrstuvwyz"
    letra_aleatoria = random.choice(char)
    upload_folder = 'dir/' + letra_aleatoria
    APLIC_BIRD.config['upload_folder'] = upload_folder
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s', filename="log.txt") #basicConfig usa relase an reque
    try:
        if request.method == 'POST':
            dir_ip = request.remote_addr
            prov = request.form.get("ubi")
            hilo = threading.current_thread().getName()
            time = dt.datetime.now()
            log.log(hilo, prov, dir_ip, time)
            file = request.files['file']
            try:
                if file and allowed_file(file.filename):
                    image_path = "static/imagenes/mov"
                    print('**archivo encontrado', file.filename)
                    filename = secure_filename(file.filename)
                    os.mkdir(upload_folder)
                    file.save(os.path.join(APLIC_BIRD.config['upload_folder'], filename))
                    main(upload_folder, filename)
                    final.unir(upload_folder, image_path, filename)
                    return redirect(url_for('imagenes',upload_folder=upload_folder, image_path=image_path, filename=filename) )
            except FileNotFoundError:
                print("El archivo no se pudo encontrar")
    except TypeError:
        print("El proceso no acepta el metodo seleccionado.")

        
    return '''
    <!doctype html>
    <title>Bird_Detection</title>
    <h1 style="text-align: center;"><span style="color: #339966;"><strong>BIRD DETECTION</strong></span></h1>
<p><strong><img style="display: block; margin-left: auto; margin-right: auto;" src="https://cdn.download.ams.birds.cornell.edu/api/v1/asset/251979231/" alt="" width="423" height="238" /><br /></strong></p>
<p>&nbsp;</p>
<form action="" enctype="multipart/form-data" method="post">
<p style="text-align: center;"> Seleccioná de tu ordenador el video a procesar </p>
<p style="text-align: center;"><input name="file" type="file" /></p>
<p style="text-align: center;"> ¿Desde dónde estas utilizando nuestra app? </p>
<p style="text-align: center;"> 

<select name="ubi">
<option value="ARGENTINA">ARGENTINA</option>
<option value="ESPAÑA">ESPAÑA</option>

</select>
</p>


<h4 style="color: #317399;text-align: center;">PARA IR VISUALIZANDO CADA FOTOGRAMA EN MOVIMIENTO , UTILIZÁ LA TECLA "ENTER" LUEGO DE QUE APAREZCA LA VENTANA DE FOTOGRAMAS</h4>
<p style="text-align: center;">&nbsp;</p>
<p style="text-align: center;"><input type="submit" value="PROCESAR VIDEO" /></p>
</form>
    '''
if __name__ == '__main__':
    APLIC_BIRD.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
