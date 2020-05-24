import os
import subprocess
from flask import Flask, request, render_template, send_file
from config import BaseConfig
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(BaseConfig)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in BaseConfig.ALLOWED_EXTENSIONS

def change_ending(filename, ending):
    return "{0}.{1}".format(os.path.splitext(filename)[0], ending)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        if 'file' not in request.files:
            return "Invalid request", 400

        file = request.files['file']

        if not file.filename or file.filename == '':
            return "Invalid request", 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            ofx_filename = change_ending(filename, 'ofx')
            ofx_filepath = os.path.join(app.config['UPLOAD_FOLDER'], ofx_filename)

            subprocess.call(["ofxstatement", "convert", "-t", "op:eur", filepath, ofx_filepath])

            return send_file(ofx_filepath, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)