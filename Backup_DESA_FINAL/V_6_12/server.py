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
import logging



#print digits + chars


#char = "abcdefghijklmnñopqrstuvwyz"
#letra_aleatoria = random.choice(char)

#UPLOAD_FOLDER = 'dir/' + letra_aleatoria

ALLOWED_EXTENSIONS = set(['mov', 'avi', 'mkv','mp4'])

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#traigo de los otros modulos (es lo mismo de main.py)

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




def muestra(q,q2):
    while True:
        ubi=q2.get()
        if not q.empty():
            #print("rutaaaa",ubi)
            read = q.get()
            #print("desde el proceso muestra",read)
            
            image_path= (ubi +'/'+read)
            #print("image_path",image_path)
            
            
            img = cv2.imread(image_path) 
            window_width=800 #size of the display window on the screen
            window_height=600

           
            cv2.namedWindow("BIRD DETECTION", cv2.WINDOW_NORMAL)

            
            cv2.resizeWindow("BIRD DETECTION", window_width, window_height)

            

            cv2.imshow("BIRD DETECTION",img) 

            
            cv2.waitKey(0) 

            
            cv2.destroyAllWindows() 

        


            #q2.put(read)
            #return url_for('uploaded_file',filename=read)
            #return read
            

    #return url_for('uploaded_file',filename=filename)
            #return 0
    


def main(dir,filename):
    #t1 = threading.Thread(name="h1", target=fotogramas.dividir, args=(dir+'/'+filename,))
    q = multiprocessing.Queue()

    q2 = multiprocessing.Queue()

    p = multiprocessing.Process(target=fotogramas.dividir, args=(dir+'/'+filename,))
    
    p2 = multiprocessing.Process(target=algoritmo.compara, args=(dir+'/'+filename,q,q2,))

    p3=multiprocessing.Process(target=muestra, args=(q,q2,))

    

    p.start()
    p.join()
    p2.start()
    p3.start()
    p2.join()
    
    #while True:
        #if not q2.empty():
            #final = q2.get()
            #print("final es", final)
            
            #url_for('uploaded_file',filename=final)

    #print(read)

    #funcion que busca los archivos -> directorio 




#fin de traer los otros modulos


def allowed_file(filename):

    #logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s' )
  
    return filename[-3:].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    char = "abcdefghijklmnñopqrstuvwyz"
    letra_aleatoria = random.choice(char)
    #print(letra_aleatoria)
    UPLOAD_FOLDER = 'dir/' + letra_aleatoria
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    a = logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s', filename="log.txt") #basicConfig usa relase an reque
    
    if request.method == 'POST':
        prov = request.form.get("ubi")
        ubicacion = threading.current_thread().getName()
        #x = threading.Thread(target=log, args=(ubicacion,))
        log(ubicacion,prov)
        
        #print(ubicacion)
        file = request.files['file']
        if file and allowed_file(file.filename):
            print ('**archivo encontrado', file.filename)
            filename = secure_filename(file.filename)
            os.mkdir(UPLOAD_FOLDER)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main(UPLOAD_FOLDER,filename)
            #print(final)
            return redirect(url_for('uploaded_file'))


        
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
<option value="AF">Afganistán</option>
<option value="AL">Albania</option>
<option value="DE">Alemania</option>
<option value="AD">Andorra</option>
<option value="AO">Angola</option>
<option value="AI">Anguilla</option>
<option value="AQ">Antártida</option>
<option value="AG">Antigua y Barbuda</option>
<option value="AN">Antillas Holandesas</option>
<option value="SA">Arabia Saudí</option>
<option value="DZ">Argelia</option>
<option value="AR">Argentina</option>
<option value="AM">Armenia</option>
<option value="AW">Aruba</option>
<option value="AU">Australia</option>
<option value="AT">Austria</option>
<option value="AZ">Azerbaiyán</option>
<option value="BS">Bahamas</option>
<option value="BH">Bahrein</option>
<option value="BD">Bangladesh</option>
<option value="BB">Barbados</option>
<option value="BE">Bélgica</option>
<option value="BZ">Belice</option>
<option value="BJ">Benin</option>
<option value="BM">Bermudas</option>
<option value="BY">Bielorrusia</option>
<option value="MM">Birmania</option>
<option value="BO">Bolivia</option>
<option value="BA">Bosnia y Herzegovina</option>
<option value="BW">Botswana</option>
<option value="BR">Brasil</option>
<option value="BN">Brunei</option>
<option value="BG">Bulgaria</option>
<option value="BF">Burkina Faso</option>
<option value="BI">Burundi</option>
<option value="BT">Bután</option>
<option value="CV">Cabo Verde</option>
<option value="KH">Camboya</option>
<option value="CM">Camerún</option>
<option value="CA">Canadá</option>
<option value="TD">Chad</option>
<option value="CL">Chile</option>
<option value="CN">China</option>
<option value="CY">Chipre</option>
<option value="VA">Ciudad del Vaticano (Santa Sede)</option>
<option value="CO">Colombia</option>
<option value="KM">Comores</option>
<option value="CG">Congo</option>
<option value="CD">Congo, República Democrática del</option>
<option value="KR">Corea</option>
<option value="KP">Corea del Norte</option>
<option value="CI">Costa de Marfíl</option>
<option value="CR">Costa Rica</option>
<option value="HR">Croacia (Hrvatska)</option>
<option value="CU">Cuba</option>
<option value="DK">Dinamarca</option>
<option value="DJ">Djibouti</option>
<option value="DM">Dominica</option>
<option value="EC">Ecuador</option>
<option value="EG">Egipto</option>
<option value="SV">El Salvador</option>
<option value="AE">Emiratos Árabes Unidos</option>
<option value="ER">Eritrea</option>
<option value="SI">Eslovenia</option>
<option value="ES" selected>España</option>
<option value="US">Estados Unidos</option>
<option value="EE">Estonia</option>
<option value="ET">Etiopía</option>
<option value="FJ">Fiji</option>
<option value="PH">Filipinas</option>
<option value="FI">Finlandia</option>
<option value="FR">Francia</option>
<option value="GA">Gabón</option>
<option value="GM">Gambia</option>
<option value="GE">Georgia</option>
<option value="GH">Ghana</option>
<option value="GI">Gibraltar</option>
<option value="GD">Granada</option>
<option value="GR">Grecia</option>
<option value="GL">Groenlandia</option>
<option value="GP">Guadalupe</option>
<option value="GU">Guam</option>
<option value="GT">Guatemala</option>
<option value="GY">Guayana</option>
<option value="GF">Guayana Francesa</option>
<option value="GN">Guinea</option>
<option value="GQ">Guinea Ecuatorial</option>
<option value="GW">Guinea-Bissau</option>
<option value="HT">Haití</option>
<option value="HN">Honduras</option>
<option value="HU">Hungría</option>
<option value="IN">India</option>
<option value="ID">Indonesia</option>
<option value="IQ">Irak</option>
<option value="IR">Irán</option>
<option value="IE">Irlanda</option>
<option value="BV">Isla Bouvet</option>
<option value="CX">Isla de Christmas</option>
<option value="IS">Islandia</option>
<option value="KY">Islas Caimán</option>
<option value="CK">Islas Cook</option>
<option value="CC">Islas de Cocos o Keeling</option>
<option value="FO">Islas Faroe</option>
<option value="HM">Islas Heard y McDonald</option>
<option value="FK">Islas Malvinas</option>
<option value="MP">Islas Marianas del Norte</option>
<option value="MH">Islas Marshall</option>
<option value="UM">Islas menores de Estados Unidos</option>
<option value="PW">Islas Palau</option>
<option value="SB">Islas Salomón</option>
<option value="SJ">Islas Svalbard y Jan Mayen</option>
<option value="TK">Islas Tokelau</option>
<option value="TC">Islas Turks y Caicos</option>
<option value="VI">Islas Vírgenes (EEUU)</option>
<option value="VG">Islas Vírgenes (Reino Unido)</option>
<option value="WF">Islas Wallis y Futuna</option>
<option value="IL">Israel</option>
<option value="IT">Italia</option>
<option value="JM">Jamaica</option>
<option value="JP">Japón</option>
<option value="JO">Jordania</option>
<option value="KZ">Kazajistán</option>
<option value="KE">Kenia</option>
<option value="KG">Kirguizistán</option>
<option value="KI">Kiribati</option>
<option value="KW">Kuwait</option>
<option value="LA">Laos</option>
<option value="LS">Lesotho</option>
<option value="LV">Letonia</option>
<option value="LB">Líbano</option>
<option value="LR">Liberia</option>
<option value="LY">Libia</option>
<option value="LI">Liechtenstein</option>
<option value="LT">Lituania</option>
<option value="LU">Luxemburgo</option>
<option value="MK">Macedonia, Ex-República Yugoslava de</option>
<option value="MG">Madagascar</option>
<option value="MY">Malasia</option>
<option value="MW">Malawi</option>
<option value="MV">Maldivas</option>
<option value="ML">Malí</option>
<option value="MT">Malta</option>
<option value="MA">Marruecos</option>
<option value="MQ">Martinica</option>
<option value="MU">Mauricio</option>
<option value="MR">Mauritania</option>
<option value="YT">Mayotte</option>
<option value="MX">México</option>
<option value="FM">Micronesia</option>
<option value="MD">Moldavia</option>
<option value="MC">Mónaco</option>
<option value="MN">Mongolia</option>
<option value="MS">Montserrat</option>
<option value="MZ">Mozambique</option>
<option value="NA">Namibia</option>
<option value="NR">Nauru</option>
<option value="NP">Nepal</option>
<option value="NI">Nicaragua</option>
<option value="NE">Níger</option>
<option value="NG">Nigeria</option>
<option value="NU">Niue</option>
<option value="NF">Norfolk</option>
<option value="NO">Noruega</option>
<option value="NC">Nueva Caledonia</option>
<option value="NZ">Nueva Zelanda</option>
<option value="OM">Omán</option>
<option value="NL">Países Bajos</option>
<option value="PA">Panamá</option>
<option value="PG">Papúa Nueva Guinea</option>
<option value="PK">Paquistán</option>
<option value="PY">Paraguay</option>
<option value="PE">Perú</option>
<option value="PN">Pitcairn</option>
<option value="PF">Polinesia Francesa</option>
<option value="PL">Polonia</option>
<option value="PT">Portugal</option>
<option value="PR">Puerto Rico</option>
<option value="QA">Qatar</option>
<option value="UK">Reino Unido</option>
<option value="CF">República Centroafricana</option>
<option value="CZ">República Checa</option>
<option value="ZA">República de Sudáfrica</option>
<option value="DO">República Dominicana</option>
<option value="SK">República Eslovaca</option>
<option value="RE">Reunión</option>
<option value="RW">Ruanda</option>
<option value="RO">Rumania</option>
<option value="RU">Rusia</option>
<option value="EH">Sahara Occidental</option>
<option value="KN">Saint Kitts y Nevis</option>
<option value="WS">Samoa</option>
<option value="AS">Samoa Americana</option>
<option value="SM">San Marino</option>
<option value="VC">San Vicente y Granadinas</option>
<option value="SH">Santa Helena</option>
<option value="LC">Santa Lucía</option>
<option value="ST">Santo Tomé y Príncipe</option>
<option value="SN">Senegal</option>
<option value="SC">Seychelles</option>
<option value="SL">Sierra Leona</option>
<option value="SG">Singapur</option>
<option value="SY">Siria</option>
<option value="SO">Somalia</option>
<option value="LK">Sri Lanka</option>
<option value="PM">St Pierre y Miquelon</option>
<option value="SZ">Suazilandia</option>
<option value="SD">Sudán</option>
<option value="SE">Suecia</option>
<option value="CH">Suiza</option>
<option value="SR">Surinam</option>
<option value="TH">Tailandia</option>
<option value="TW">Taiwán</option>
<option value="TZ">Tanzania</option>
<option value="TJ">Tayikistán</option>
<option value="TF">Territorios franceses del Sur</option>
<option value="TP">Timor Oriental</option>
<option value="TG">Togo</option>
<option value="TO">Tonga</option>
<option value="TT">Trinidad y Tobago</option>
<option value="TN">Túnez</option>
<option value="TM">Turkmenistán</option>
<option value="TR">Turquía</option>
<option value="TV">Tuvalu</option>
<option value="UA">Ucrania</option>
<option value="UG">Uganda</option>
<option value="UY">Uruguay</option>
<option value="UZ">Uzbekistán</option>
<option value="VU">Vanuatu</option>
<option value="VE">Venezuela</option>
<option value="VN">Vietnam</option>
<option value="YE">Yemen</option>
<option value="YU">Yugoslavia</option>
<option value="ZM">Zambia</option>
<option value="ZW">Zimbabue</option>
</select>
</p>


<h4 style="color: #317399;text-align: center;">PARA IR VISUALIZANDO CADA FOTOGRAMA EN MOVIMIENTO , UTILIZÁ LA TECLA "ENTER" LUEGO DE QUE APAREZCA LA VENTANA DE FOTOGRAMAS</h4>
<p style="text-align: center;">&nbsp;</p>
<p style="text-align: center;"><input type="submit" value="PROCESAR VIDEO" /></p>
</form>
    '''
    
@app.route('/uploaded_file')
def uploaded_file():
    
    
    return '''
    <!doctype html>
    <title>Bird_Detection</title>
    <h1 style="text-align: center;"><span style="color: #339966;"><strong>GRACIAS POR UTILIZAR LA APP "BIRD DETECTION"</strong></span></h1>
<p><strong><img style="display: block; margin-left: auto; margin-right: auto;" src="https://cdn.download.ams.birds.cornell.edu/api/v1/asset/251979231/" alt="" width="423" height="238" /><br /></strong></p>
<p>&nbsp;</p>

    '''


if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
    
