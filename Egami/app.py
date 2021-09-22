from flask import Flask,request,flash,redirect,render_template
import os
import io
import base64

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'uploads/'
app = Flask (__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'asdasd'


@app.route("/")
def home():
    return render_template("index.html")

from PIL import Image, ImageOps

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():

    if 'file' not in request.files:
        flash('No file part')
        return render_template('index.html')

    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return render_template('index.html')

    if file and allowed_file(file.filename):

        im = Image.open(file)
        im = ImageOps.invert(im)
        im = ImageOps.flip(im)

        b = io.BytesIO()
        im.save(b, 'jpeg')
        im_bytes = b.getvalue()

        image_string = base64.b64encode(im_bytes).decode("utf-8")

        return render_template('index.html',uploaded_image = image_string)
    else:
        return render_template('index.html')
