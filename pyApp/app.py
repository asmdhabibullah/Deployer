import os
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_json import FlaskJSON, as_json, json_response
from torchserve import default_args, start_ts, connect
from torch_model_archiver import model_packaging_utils
from torchserve.model import Model

app = Flask(__name__)
FlaskJSON(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def archive_model(mdl_url, model_name, version, serialized_file, model_file, handler, extra_files):
    tmp_dir = os.path.join(os.getcwd(), 'tmp')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    mdl_url = '{}/{}.pth'.format(mdl_url, model_name)
    mdl_path = os.path.join(tmp_dir, '{}.pth'.format(model_name))
    model_packaging_utils.load_url(mdl_url, mdl_path)

    archive_dir = os.path.join(os.getcwd(), 'storages', model_name)
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    model_packaging_args = {
        'model_name': model_name,
        'version': version,
        'serialized_file': serialized_file,
        'model_file': model_file,
        'handler': handler,
        'extra_files': [extra_files],
        'export_path': archive_dir
    }

    model_packaging_utils.package_model(**model_packaging_args)

    return 'Model archive created at {}'.format(archive_dir)

def register_model_with_torchserve(model_name, model_file, serialized_file, handler):
    # Check if TorchServe is already running
    try:
        conn = connect()
        models = conn.get_model_names()
    except Exception:
        models = []

    if model_name not in models:
        # Start TorchServe with default arguments
        args = default_args()
        start_ts(args)

    # Register the model with TorchServe
    model = Model(model_name, model_file, serialized_file=serialized_file, handler=handler)
    model.register()

@app.route('/api/v1/models', methods=['POST'])
def archive_and_register_model():
    data = request.json
    model_name = data['model_name']
    version = data['version']
    serialized_file = data['serialized_file']
    model_file = data['model_file']
    handler = data['handler']
    extra_files = data['extra_files']

    archive_model(model_name, version, serialized_file, model_file, handler, extra_files)
    register_model_with_torchserve(model_name, model_file, serialized_file, handler)

    return jsonify({'message': 'Model archived and registered successfully'})

@app.route('/api/v1/models', methods=['GET'])
def get_models_status():
    conn = connect()
    models = conn.get_model_names()
    status = []

    for model in models:
        health = conn.get_model_health(model)
        status.append({
            'model_name': model,
            'status': 'Healthy' if health == 'HEALTHY' else 'Unhealthy',
            'url': 'http://localhost:8080/predictions/{}'.format(model)
        })

    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="3520")