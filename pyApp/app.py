import os
import json
import torch
import requests
from flask_cors import CORS
from flask_json import FlaskJSON
# from handeler import ModelHandler
from flask import Flask, request, jsonify
from torch_model_archiver import ModelArchiver


app = Flask(__name__)
FlaskJSON(app)

CORS(app, resources={r"/api/*": {"origins": "*"}})

# Define your PyTorch model
class MyModel(torch.nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        # Define your model layers and operations here

    def forward(self, x):
        # Define the forward pass of your model
        # x: input tensor
        # return: output tensor
        pass


def archive_model(model_name, serialized_file, model_file, handler, extra_files, version):
    # Create an instance of your PyTorch model
    model = MyModel()

    # Save the model's state dictionary to the serialized file
    torch.save(model.state_dict(), serialized_file)

    # Define the path to save the model archive
    archive_dir = os.path.join(os.getcwd(), '/pyApp/storages', model_name)

    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    model_archiver = ModelArchiver()

    # Archive the model
    model_archiver.archive_model(model_name='my_model',
                                version='1.0',
                                serialized_file=serialized_file,
                                model_file='model.py',
                                handler='handler.py',
                                export_path=archive_dir)

    
    # # Create an instance of ModelArchiver
    # model_archiver = ModelArchiver()

    # # Archive the model
    # model_archiver.archive_model(model_name=model_name,
    #                             version=version,
    #                             serialized_file=serialized_file,
    #                             model_file=model_file,
    #                             handler=handler,
    #                             export_path=extra_files)
    # model_archiver = ModelArchiver()

    # tmp_dir = os.path.join(os.getcwd(), './app/storages')

    # if not os.path.exists(tmp_dir):
    #     os.makedirs(tmp_dir)

    # # Archive the model using ModelArchiver
    # archive_dir = os.path.join(os.getcwd(), './app/storages', model_name)
    # model_archiver.archive_model(model_name=model_name,
    #                              version=version,
    #                              serialized_file=serialized_file,
    #                              model_file=model_file,
    #                              handler=handler,
    #                              extra_files=[extra_files],
    #                              export_path=archive_dir)
    
    # data = request.json
    # model_name = data['model_name']
    # version = data['version']
    # serialized_file = data['serialized_file']
    # model_file = data['model_file']
    # handler = data['handler']
    # extra_files = data['extra_files']

    # Register the model (implement this function)
    # register_model(model_name, model_file, serialized_file, handler)


    # mdl_url = '{}/{}.pth'.format(mdl_url, model_name)
    # mdl_path = os.path.join(tmp_dir, '{}.pth'.format(model_name))
    # load_url(mdl_url, mdl_path)

    # archive_dir = os.path.join(os.getcwd(), 'storages', model_name)
    # if not os.path.exists(archive_dir):
    #     os.makedirs(archive_dir)

    # model_packaging_args = {
    #     'model_name': model_name,
    #     'version': version,
    #     'serialized_file': serialized_file,
    #     'model_file': model_file,
    #     'handler': handler,
    #     'extra_files': [extra_files],
    #     'export_path': archive_dir
    # }

    # package_model(**model_packaging_args)

    # return 'Model archive created at {}'.format(archive_dir)

def validate_data(data, keys_to_validate):
    errors = {}
    for key in keys_to_validate:
        if key not in data or not data[key]:
            errors[key] = f"Missing or empty value for {key}"
    return len(errors) == 0, errors

@app.route('/api/v1/models', methods=['POST'])
def archive_and_register_model():

    data = request.json

    keys_to_validate = ['mdl_name', 'version', 'ser_file', 'mdl_file', 'hdl_file', 'ext_file']

    valid, errors = validate_data(data, keys_to_validate)

    print(errors)

    if not valid:
        return jsonify({'errors': errors}), 400  # Return error response with status code 400

    model_name = data['mdl_name']
    version = data['version']
    serialized_file = data['ser_file']
    model_file = data['mdl_file']
    handler = data['hdl_file']
    extra_files = data['ext_file']



    archive_model(model_name, version, serialized_file, model_file, handler, extra_files)
    # model_handler = ModelHandler()
    # model_handler.initialize(context={'model_dir': os.path.join(os.getcwd(), 'storages', model_name)})
    # register_model(model_name, model_file, serialized_file, handler)

    return jsonify({'message': 'Model archived and registered successfully'})

@app.route('/api/v1/models', methods=['GET'])
def get_models_status():
    response = requests.get('http://localhost:8080/models')
    models = response.json()
    status = []

    for model in models:
        model_name = model['modelName']
        model_status = model['status']
        # model_handler = ModelHandler()
        model_handler.initialize(context={'model_dir': os.path.join(os.getcwd(), 'storages', model_name)})
        status.append({
            'model_name': model_name,
            'status': model_status,
            'url': f'http://localhost:8080/predictions/{model_name}'
        })

    return jsonify(status)


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="3520")


# def register_model_with_torchserve(model_name, model_file, serialized_file, handler):
#     # Check if TorchServe is already running
#     try:
#         conn = connect()
#         models = conn.get_model_names()
#     except Exception:
#         models = []

#     if model_name not in models:
#         # Start TorchServe with default arguments
#         args = default_args()
#         start_ts(args)

#     # Register the model with TorchServe
#     model = Model(model_name, model_file, serialized_file=serialized_file, handler=handler)
#     model.register()

# @app.route('/api/v1/models', methods=['GET'])
# def get_models_status():
#     conn = connect()
#     models = conn.get_model_names()
#     status = []

#     for model in models:
#         health = conn.get_model_health(model)
#         status.append({
#             'model_name': model,
#             'status': 'Healthy' if health == 'HEALTHY' else 'Unhealthy',
#             'url': 'http://localhost:8080/predictions/{}'.format(model)
#         })

#     return jsonify(status)

#     data = request.json
#     model_name = data['model_name']
#     serialized_file = data['serialized_file']
#     model_file = data['model_file']
#     handler = data['handler']

#     start_torchserve()

#     # Register the model with TorchServe
#     command = f"torchserve --model-name={model_name} --serialized-file={serialized_file} --model-file={model_file} --handler={handler}"
#     subprocess.Popen(command.split())

#     return jsonify({'message': 'Model registered successfully'})
# torchserve_process = None

# def start_torchserve():
#     global torchserve_process
#     if torchserve_process is None or torchserve_process.poll() is not None:
#         # Start TorchServe with default arguments
#         command = 'torchserve --start'
#         torchserve_process = subprocess.Popen(command.split())

# # @app.route('/api/v1/models', methods=['POST'])
# def register_model():