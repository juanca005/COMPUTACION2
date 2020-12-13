#!/usr/bin/python3
# -*- coding: utf-8 -*-


from librerias import *
from flask import render_template

ALLOWED_EXTENSIONS = set(['mov', 'avi', 'mkv','mp4'])

app = Flask(__name__)



def main(dir,filename):
    #t1 = threading.Thread(name="h1", target=fotogramas.dividir, args=(dir+'/'+filename,))
    q = multiprocessing.Queue()

    q2 = multiprocessing.Queue()

    p = multiprocessing.Process(target=fotogramas.dividir, args=(dir+'/'+filename,))
    
    p2 = multiprocessing.Process(target=algoritmo.compara, args=(dir+'/'+filename,q,q2,))
    


    #p3=multiprocessing.Process(target=mostrar.muestra, args=(q,q2,))

    
    p.start()
    p.join()
    p2.start()
    #p3.start()
    p2.join()

    #imagen=q.get()
    ruta=q2.get()
    print ("rutaaaaaaaaaaaaaaa colaaa",ruta)
    #return ruta
    #return url_for('imagenes',ruta=ruta)
    

#intentos


@app.route('/mostrar' , methods=["GET"])
def imagenes():
    #print(carpeta)
    name= request.form.get("ubi")
    print(name)

    image_path="static/imagenes/mov/dir"
    image_path2="o/video_corto.mp4"

    path_final = os.path.join(image_path , image_path2)

    pics = os.listdir(path_final)

    return render_template("mostrar.html",ruta=path_final,pics=pics)



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
        ip = request.remote_addr
        prov = request.form.get("ubi")
        hilo = threading.current_thread().getName()
        time = dt.datetime.now()
        #x = threading.Thread(target=log, args=(ubicacion,))
        log.log(hilo,prov,ip,time)
        
        #print(ubicacion)
        file = request.files['file']
        if file and allowed_file(file.filename):
            print ('**archivo encontrado', file.filename)
            filename = secure_filename(file.filename)
            os.mkdir(UPLOAD_FOLDER)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            main(UPLOAD_FOLDER,filename)
            #print(ruta)
         
            return redirect(url_for('imagenes'))
            #send_from_directory('static', filename)


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
    
@app.route('/uploaded_file')
def uploaded_file():

    print("algoo")
    
    #@app.route('/mov/dir/d/<filename>')
    #def uploaded_file(filename):
    
    
    #return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    
    return '''
    <!doctype html>
    <title>Bird_Detection</title>
    <h1 style="text-align: center;"><span style="color: #339966;"><strong>GRACIAS POR UTILIZAR LA APP "BIRD DETECTION"</strong></span></h1>
<p><strong><img style="display: block; margin-left: auto; margin-right: auto;" src="https://cdn.download.ams.birds.cornell.edu/api/v1/asset/251979231/" alt="" width="423" height="238" /><br /></strong></p>
<p>&nbsp;</p>

<form action="/">

<p style="text-align: center;"><input type="submit" value="MENU PRINCIPAL" /></p>
</form>

    '''


if __name__ == '__main__':
    
    app.run(host="0.0.0.0" , port=8080, threaded=True, debug=True)

    
    
