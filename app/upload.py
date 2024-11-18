import os
from flask import Blueprint, request, jsonify
from flask_cors import CORS
import shutil
from .decorator import login_required
from .deploy_docker import process
from .query import query_db
import zipfile

upload = Blueprint('upload', __name__)

CORS(upload, resources={r"/*": {"origins": "http://localhost:5173"}})

@upload.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "File tidak ada"}), 400
    
    file = request.files['file']
    token = request.form.get('token')
    port = request.form.get('port')

    if file.filename == '':
        return jsonify({"error": "File tidak ada"}), 400
    
    if file and file.filename.endswith('.zip'):
        file.save(file.filename)

        app_name = file.filename.replace(".zip","")

        shutil.move(file.filename,f'D:/Mini Project/File_Deploy/Folder_{app_name}/{file.filename}')
        with zipfile.ZipFile(f'D:/Mini Project/File_Deploy/Folder_{app_name}/{file.filename}', 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(f'D:/Mini Project/File_Deploy/Folder_{app_name}/{file.filename}'))

        process(app_name, token, port)

        return jsonify({"message": "File berhasil di upload"}), 200
    
    else:
        return jsonify({"error": "Tipe file tidak valid, hanya diperbolehkan format zip"}), 400