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

UPLOAD_FOLDER = 'dir'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
  
    return filename[-3:].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print ('**archivo encontrado', file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          
            return url_for('uploaded_file',
                                    filename=filename)
    return '''
    <!doctype html>
    <title>CARGA DE VIDEO</title>
    <h1>CARGAR NUEVO VIDEO</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p>
     
      <input type=file name=file>
         <input type=submit value=CARGAR>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)