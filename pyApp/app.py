import os
import json
import requests
import subprocess
from flask_cors import CORS
from flask_json import FlaskJSON
from flask import Flask, request, jsonify

app = Flask(__name__)
FlaskJSON(app)

CORS(app, resources={r"/api/*": {"origins": "*"}})

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
        # 'custom_handler': 'my_custom_handler.CustomHandler',
    }

    with open(file, 'w') as file:
        for key, value in config_options.items():
            file.write(f"{key}={value}\n")

def create_metadata_file(model_dir, archive_path, model_name, version):
    metadata = {
        "version": version,
        "model_name": f"{model_name}",
        "handler": f"{model_dir}/handler.py",
        "extra_files": f"{model_dir}/extra_file.txt",
        "serialized_file": f"{model_dir}/serialized_file.pt",
        "archived_file": f"{archive_path}/{model_name}.mar",
    }

    metadata_file = os.path.join(model_dir, 'metadata.json')

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f)
    # return metadata_file

    print("Metadata File Created...")

def is_torchserve_running():
    try:
        output = subprocess.check_output(['torchserve', '--status'], stderr=subprocess.STDOUT, universal_newlines=True)
        return 'TorchServe is running.' in output
    except subprocess.CalledProcessError:
        return False
# Call the function to check TorchServe status

def serve_model(archive_path, model_name):
    # Start the TorchServe server using the model
    # torchserve_running = is_torchserve_running()

    if not is_torchserve_running():
        start_torchserve_cmd = f"torchserve --start --ncs --model-store {archive_path} --models {model_name}={model_name}.mar --ts-config {archive_path}/{model_name}.config.properties"
        os.system(start_torchserve_cmd)
    else:
        attached_model_cmd = f"torchserve --model-store {archive_path} --models {model_name}={model_name}.mar --ts-config {archive_path}/{model_name}.config.properties"
        os.system(attached_model_cmd)

    url = f"http://localhost:8081/models/{model_name}"
    
    response = requests.get(url)

    print("response", response)

    # return response.json()
    print("PyTorch Serve Started")

@app.route('/api/v1/model/create', methods=['POST'])
def upload_files_create_model():
    # Create a "models" directory if it doesn't exist
    if not os.path.exists(os.path.join('models')):
        os.makedirs('models')

    data = request.form.to_dict(flat=False)
    # print(request.files)

    version = data['version'][0] if isinstance(data, dict) else data['version']
    model_name = data['mdl_name'][0] if isinstance(data, dict) else data['mdl_name']
    model_file = request.files['mdl_file']
    serialized_file = request.files['ser_file']
    handler_file = request.files['hdl_file']
    extra_file = request.files['ext_file']

    new_data = {
        'mdl_name': model_name,
        'version': version,
        'ser_file': model_file,
        'mdl_file': serialized_file,
        'hdl_file': handler_file,
        'ext_file': extra_file
    }

    keys_to_validate = ['mdl_name', 'version', 'ser_file', 'mdl_file', 'hdl_file', 'ext_file']

    valid, errors = validate_data(new_data, keys_to_validate)

    if not valid:
        print("Errors")
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

    return jsonify({'message': 'Model uploaded and served successfully.'})

def get_model_info():
    url = 'http://localhost:8080/models'
    response = requests.get(url)

    print("response", response)

    if response.status_code == 200:
        models = json.loads(response.text)
        model_info = []
        for model in models:
            model_info.append({
                'model_name': model['modelName'],
                'model_url': model['modelUrl'],
                'runtime': model['runtime'],
                'min_workers': model['minWorkers'],
                'max_workers': model['maxWorkers'],
                'batch_size': model['batchSize'],
                'status': model['status'],
                'health': model['health']
            })
        return model_info
    else:
        return None

@app.route('/api/v1/model', methods=['GET'])
def get_all_model_info():
    model_info = get_model_info()
    if model_info is not None:
        return jsonify(model_info), 200
    return jsonify({'message': 'Model can"t find in the storage folder.'}), 404

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="3520")