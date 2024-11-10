import os
from flask import Blueprint, request, jsonify
from flask_cors import CORS
import shutil

upload = Blueprint('upload', __name__)

CORS(upload, resources={r"/*": {"origins": "http://localhost:5173"}})

@upload.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "File tidak ada"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "File tidak ada"}), 400
    
    if file and file.filename.endswith('.zip'):
        file.save(file.filename)

        shutil.move(f'{file.filename}',f'D:/Mini Project/File_Deploy/Folder_{file.filename}/{file.filename}')

        return jsonify({"message": "File berhasil di upload"}), 200
    
    else:
        return jsonify({"error": "Tipe file tidak valid, hanya diperbolehkan format zip"}), 400