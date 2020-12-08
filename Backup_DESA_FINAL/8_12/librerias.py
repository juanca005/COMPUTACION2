#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
import re
import math
import sys, getopt
from os.path import basename
from PIL import Image
from urllib.request import urlopen
import urllib.request
import requests
import array
from concurrent.futures import ProcessPoolExecutor
import io
from os import remove
import os, shutil
import multiprocessing
from multiprocessing import Process, Queue
import cgi
from http.server import BaseHTTPRequestHandler
from flask import Flask, request, redirect, url_for, send_from_directory
import werkzeug 
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import time
from concurrent.futures import ThreadPoolExecutor
import fotogramas
import algoritmo
import random
import string
from flask import send_from_directory
from flask import send_file
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import mostrar
import log