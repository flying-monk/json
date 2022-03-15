import os
import os.path
from datetime import datetime
from wsgiref.util import request_uri
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import json

UPLOAD_FOLDER = 'file/'
# ALLOWED_EXTENSIONS = {'txt', 'waypoints', 'plan', 'mission'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload():
    return render_template("upload.html")

@app.route('/success', methods=['GET', 'POST']) 
def success(): 
    if request.method=='POST':
        upload_file = request.files['file']
        filename = secure_filename(upload_file.filename)
        upload_file.save(app.config['UPLOAD_FOLDER'] + filename)
        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()
    return render_template("success.html", name=upload_file.filename)

@app.route('/test', methods=['GET'])
def test():
    data = request.json
    print(data)
    current_time = datetime.datetime.now()
    microsecond = current_time.microsecond
    filename = 'datafile'+str(microsecond)+'.json'
    file_exists = os.path.exists(filename)
    if not file_exists:
        file = open(filename, 'w')
        file.write(json.dumps(data))
        file.close()
    return jsonify(data)



if __name__ == "__main__":
    app.run(port=2727, debug=True)