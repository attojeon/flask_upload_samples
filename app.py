import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
# from gevent.pywsgi import WSGIServer
from teachable_machine import TeachableMachine


# # Some utilites
# import numpy as np
from util import base64_to_pil, png_name

# 모델 로딩
my_model = TeachableMachine(model_path = 'keras_model.h5', model_type='h5')


app = Flask(__name__)
save_path = os.path.join(app.root_path,  "upload_dir")

def show_appinfo():
   print("#"*80)
   print(f">>> app.root_path : {app.root_path} ")
   print(f">>> app.static_folder : {app.static_folder}")
   print(f">>> app.static_url_path : {app.static_url_path}")
   print(f">>> app.template_folder : {app.template_folder}")
   print("#"*80)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def render_upload():
    return render_template('upload.html')

@app.route('/uploads')
def render_uploads():
    return render_template('uploadbt4.html')

# 파일 업로드
@app.route('/fileupload', methods=['POST'] )
def file_upload():
    f = request.files['file']
    filename = f.filename
    os.makedirs(save_path, exist_ok=True)
    target = os.path.join(save_path, filename)
    print(f">>> upload file: {target}")
    f.save(target)
    return redirect(url_for("index"))

@app.route('/fileuploads', methods=['POST'])
def file_uploads():
    os.makedirs(save_path, exist_ok=True)
    files = request.files.getlist('file')
    for f in files:
        filename = f.filename
        target = os.path.join(save_path, filename)
        print(f">>> upload file: {target}")
        f.save(target)
    return redirect(url_for("index"))

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)

        # Save the image to ./uploads
        save_path = f'./uploads/{png_name()}'
        img.save(save_path)

        # 아토
        res = my_model.classify_image(save_path)
        print(f"이미지 이름: {save_path}, 결과: {res['highest_class_id']}")
        return jsonify(result=str( res['highest_class_id']) )
    return None 

show_appinfo()
app.run(port=8080, host='0.0.0.0') 