import os
from flask import Blueprint, request, jsonify
from flask_cors import CORS
import shutil
from .decorator import login_required
from .deploy_docker import process, check_app_slot
from .query import query_db
import zipfile

upload = Blueprint('upload', __name__)

PATH = os.getenv('DEPLOY_PATH')

CORS(upload, resources={r"/*": {"origins": "http://localhost:5173"}})

@upload.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "File tidak ada"}), 400
    
    file = request.files['file']
    token = request.form.get('token')
    srcport = request.form.get('srcport')
    dstport = request.form.get('dstport')

    if file.filename == '':
        return jsonify({"error": "File tidak ada"}), 400
    
    if file and file.filename.endswith('.zip'):
        file.save(file.filename)

        app_name = file.filename.replace(".zip","")

        result_check = check_app_slot(app_name, dstport)
        if result_check:
            return jsonify({"message": "Nama aplikasi atau port sudah terpakai"}), 400

        folder_deploy = f'{PATH}{app_name}'

        shutil.move(file.filename,f'{folder_deploy}/{file.filename}')
        with zipfile.ZipFile(f'{folder_deploy}/{file.filename}', 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(f'{folder_deploy}/{file.filename}'))

        process(app_name, token, srcport, dstport)

        return jsonify({"message": "File berhasil di upload"}), 200
    else:
        return jsonify({"message": "Tipe file tidak valid, hanya diperbolehkan format zip"}), 400