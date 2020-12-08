#!/usr/bin/python3
# -*- coding: utf-8 -*-
import io
import mimetypes
from urllib import request
import uuid
import requests


url = "http://localhost:8080/"
fin = open('video/aa.mp4', 'rb')
files = {'file': fin}
try:
    r = requests.post(url, files=files)
    print (r.text)
finally:
    fin.close()