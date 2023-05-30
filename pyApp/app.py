import os
import json
import sqlite3
import requests
import subprocess
from flask_cors import CORS
from flask_json import FlaskJSON
from flask import Flask, request, jsonify, g

app = Flask(__name__)
FlaskJSON(app)

app.config['DATABASE'] = './db/database.db'

CORS(app, resources={r"/api/*": {"origins": "*"}})

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

def init_db(version, model_name, handler_file, extra_files, serialized_file, archived_model_file, config_file, model_url, model_status):
    with app.app_context():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS model (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version TEXT,
                model_name TEXT,
                handler_file TEXT,
                extra_files TEXT,
                serialized_file TEXT,
                archived_model_file TEXT,
                config_file TEXT,
                model_url TEXT,
                model_status TEXT
            )
        """)

        # Insert data into the table
        data = {
            "version": version,
            "model_name": model_name,
            "handler_file": handler_file,
            "extra_files": extra_files,
            "serialized_file": serialized_file,
            "archived_model_file": archived_model_file,
            "config_file": config_file,
            "model_url": model_url,
            "model_status": model_status
        }

        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM model")
        count = cursor.fetchone()[0]

        if count == 0:
            db.execute("""
                INSERT INTO model (version, model_name, handler_file, extra_files, serialized_file, archived_model_file, config_file, model_url, model_status)
                VALUES (:version, :model_name, :handler_file, :extra_files, :serialized_file, :archived_model_file, :config_file, :model_url, :model_status)
            """, data)
        else:
            db.execute("""
                INSERT INTO model (version, model_name, handler_file, extra_files, serialized_file, archived_model_file, config_file, model_url, model_status)
                VALUES (:version, :model_name, :handler_file, :extra_files, :serialized_file, :archived_model_file, :config_file, :model_url, :model_status)
            """, data)

        db.commit()
        cursor.close()

def get_all_data():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''SELECT json_object(
                'id', id,
                'version', version,
                'model_name', model_name,
                'handler_file', handler_file,
                'extra_files', extra_files,
                'serialized_file', serialized_file,
                'archived_model_file', archived_model_file,
                'config_file', config_file,
                'model_url', model_url,
                'model_status', model_status
            ) FROM model''')
        rows = cursor.fetchall()

        data = []
        for row in rows:
            # print(json.loads(row[0]))
            model = json.loads(row[0])
            data.append(model)
        cursor.close()
        return data

def validate_data(data, required_keys):
    errors = []

    if isinstance(data, dict):
        # JSON data
        for key in required_keys:
            if key not in data:
                errors.append(f"Missing required field: {key}")
    else:
        # FormData data
        for key in required_keys:
            if key not in data.keys():
                errors.append(f"Missing required field: {key}")
    return len(errors) == 0, errors

def create_model_archive(model_dir, archive_path, model_name, version):
    # Use torch_model_archiver to create the model archive
    command = f"torch-model-archiver --force --model-name {model_name} --version {version} --serialized-file {os.path.join(model_dir, 'serialized_file.pt')} --handler {os.path.join(model_dir, 'handler.py')} --extra-files {os.path.join(model_dir, 'extra_file.txt')} --export-path {archive_path}"

    os.system(command)

    # return archive_path
    print("Model archived...")

def create_config_file(archive_path, model_name):

    file = os.path.join(archive_path, f"{model_name}.config.properties")

    # Config Gen
    config_options = {
        'model_name': f"{model_name}",
        'initial_workers': '1',
        'synchronous': 'true',
        'max_batch_size': '16',
        'response_timeout': '120000',
        'min_worker_threads': '1',
        'max_worker_threads': '4',
        "inference_address":"http://127.0.0.1:8080",
        "management_address": "http://127.0.0.1:8081",
        "metrics_address": "http://127.0.0.1:8082"
    }

    with open(file, 'w') as file:
        for key, value in config_options.items():
            file.write(f"{key}={value}\n")

    return file

def create_metadata_file(model_dir, archive_path, model_name, version):
    metadata = {
        "version": version,
        "model_name": f"{model_name}",
        "handler_file": f"{model_dir}/handler.py",
        "extra_files": f"{model_dir}/extra_file.txt",
        "serialized_file": f"{model_dir}/serialized_file.pt",
        "archived_model_file": f"{archive_path}/{model_name}.mar",
        "config_file" : f"{archive_path}/{model_name}.config.properties",
        "model_url": f"http://localhost:8081/models/{model_name}",
        "model_status": "Healthy"
    }

    metadata_file = os.path.join(model_dir, 'metadata.json')

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f)
    print("Metadata File Created...")

    init_db(version=metadata['version'], model_name=metadata['model_name'], handler_file=metadata['handler_file'], extra_files=metadata['extra_files'], serialized_file=metadata['serialized_file'], archived_model_file=metadata['archived_model_file'], config_file=metadata['config_file'], model_url=metadata['model_url'], model_status=metadata['model_status'])

    return metadata

def is_torchserve_running():
    try:
        command = 'curl -s http://localhost:8080/ping'
        status = os.system(command)

        # print("status", status)

        if status == 0:
            return True
        return False
        # output = subprocess.check_output(['torchserve', '--status'], stderr=subprocess.STDOUT, universal_newlines=True)
        # return 'TorchServe is running.' in output
    except subprocess.CalledProcessError:
        return False
# Call the function to check TorchServe status

def serve_model(archive_path, model_name):
    # Start the TorchServe server using the model
    # torchserve_running = is_torchserve_running()

    # print(f"is_torchserve_running: {is_torchserve_running()}")
    # print(f"archive_path: {archive_path}, model_name: {model_name}")

    if not is_torchserve_running():
        start_torchserve_cmd = f"torchserve --start --model-store {archive_path} --models {model_name}={model_name}.mar --ts-config {archive_path}/{model_name}.config.properties"
        os.system(start_torchserve_cmd)
        print("PyTorch Server Started")

    else:
        attached_model_cmd = f"torchserve --model-store {archive_path} --models {model_name}={model_name}.mar --ts-config {archive_path}/{model_name}.config.properties"
        os.system(attached_model_cmd)
        print("Model added with PyTorch Server")

    # url = f"http://localhost:8081/models/{model_name}"
    
    # response = requests.get(url)

    # print("response", response)

    # return response.json()

@app.route('/api/v1/model/create', methods=['POST'])
def upload_files_create_model():
    # Create a "models" directory if it doesn't exist
    if not os.path.exists(os.path.join('models')):
        os.makedirs('models')
    
    # form_data = request.form

    # Convert form data to JSON
    # json_data = {}
    # for key in form_data.keys():
    #     json_data[key] = form_data.get(key)

    data = request.form.to_dict(flat=False)

    # print(data)

    version = data['version'][0] if isinstance(data, dict) else data['version']
    model_name = data['mdl_name'][0] if isinstance(data, dict) else data['mdl_name']
    # version = form_data['version']
    # model_name = form_data['mdl_name']
    model_file = request.files['mdl_file']
    extra_file = request.files['ext_file']
    handler_file = request.files['hdl_file']
    serialized_file = request.files['ser_file']

    new_data = {
        'version': version,
        'mdl_name': model_name,
        'ser_file': model_file,
        'mdl_file': serialized_file,
        'hdl_file': handler_file,
        'ext_file': extra_file
    }

    # json_data["ext_file"] =extra_file
    # json_data["mdl_file"] = model_file
    # json_data["hdl_file"] =handler_file
    # json_data["ser_file"] =serialized_file


    # json_data = json.dumps(new_data)

    keys_to_validate = ['mdl_name', 'version', 'ser_file', 'mdl_file', 'hdl_file', 'ext_file']

    valid, errors = validate_data(new_data, keys_to_validate)

    if not valid:
        # print("Errors")
        return jsonify({'errors': errors}), 400  # Return error response with status code 400

    # Create a directory for the model using the model name
    model_dir = os.path.join('./models', model_name)
    archive_path = os.path.join('./storage')

    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(archive_path, exist_ok=True)

    # Save the files inside the model directory
    model_file.save(os.path.join(model_dir, model_file.filename))
    serialized_file.save(os.path.join(model_dir, 'serialized_file.pt'))
    handler_file.save(os.path.join(model_dir, 'handler.py'))
    extra_file.save(os.path.join(model_dir, 'extra_file.txt'))
    
    # create_config_file
    create_config_file(archive_path, model_name)

    # Create the model archive
    create_model_archive(model_dir, archive_path, model_name, version)

    # Create the metadata file
    create_metadata_file(model_dir, archive_path, model_name, version)

    # Serve the model
    serve_model(archive_path, model_name)

    return jsonify({'message': 'Model archivend and uploaded to serve successfully.'})

# def get_model_info():
#     # ping_url = 'http://localhost:8080/ping'
#     # ping_data = requests.get(ping_url)

#     # url = 'http://localhost:8081/models'
#     # response = requests.get(url)
#     return get_all_data()

@app.route('/api/v1/model', methods=['GET'])
def get_all_model_info():
    model_info = get_all_data()

    # print("model_info", {"message": model_info})

    if model_info is not None:
        return jsonify({"message": model_info}), 200
    return jsonify({'message': 'Model can"t find in the storage folder.'}), 404

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="3520")