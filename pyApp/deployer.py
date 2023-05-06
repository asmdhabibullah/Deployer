import os
import torch
import argparse
import subprocess
from flask_cors import CORS
from flask import Flask, request, jsonify
from torch.utils.model_zoo import load_url
from flask_json import FlaskJSON, as_json, json_response
from handler import archiver

app = Flask(__name__)
FlaskJSON(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
@as_json
def index():
    return {
        "msg": "Hey, I'm working. Your HTTP GET request accepted to process..."
    }
    # return dict(value=12)

@app.route("/api/v1/create-and-start-torch", methods=["POST"])
def archiver_pyt_model():
    content_type = request.headers.get('Content-Type')
    # mdl_archiver = ModelStorage("./models")
    # mdl_archiver.add_model()
    print("content_type", content_type)
    # parse request data
    if(content_type == "application/json"):
        body = request.get_json(force=True)
        print(body)
        # return body
    
        # print(request.files)

        version = "1.0"
        mdl_name = body['mdl_name']
        ser_file = body['ser_file']
        mdl_file = body['mdl_file']
        hdl_file = body['hdl_file']
        ext_file = body['ext_file']

        # print("mdl_name: {}, version: {}, ser_file: {}, mdl_file: {}, hdl_file: {}, ext_file: {}".format(mdl_name, version, ser_file, mdl_file, hdl_file, ext_file))
        archiver(
            mdl_name=mdl_name,
            version=version,
            ser_file=ser_file,
            mdl_file=mdl_file,
            hdl_file=hdl_file,
            ext_file=ext_file,
        )
        
        return json_response(msg="Your HTTP POST request accepted to process to start a torch server and make a torch model...")

    return {
        "msg": None
    }

    # # save uploaded files to disk
    # tmp_dir = os.path.join(os.getcwd(), 'tmp')
    # if not os.path.exists(tmp_dir):
    #     os.makedirs(tmp_dir)
    # ser_file_path = os.path.join(tmp_dir, ser_file.filename)
    # ser_file.save(ser_file_path)
    # mdl_file_path = os.path.join(tmp_dir, mdl_file.filename)
    # mdl_file.save(mdl_file_path)
    # hdl_file_path = os.path.join(tmp_dir, hdl_file.filename)
    # hdl_file.save(hdl_file_path)
    # ext_file_path = os.path.join(tmp_dir, ext_file.filename)
    # ext_file.save(ext_file_path)

    # # add model to storage
    # mdl_archiver.add_model(
    #     mdl_name=mdl_name,
    #     version=version,
    #     ser_file=ser_file_path,
    #     mdl_file=mdl_file_path,
    #     hdl_file=hdl_file_path,
    #     ext_file=ext_file_path,
    # )

    # # remove uploaded files from disk
    # os.system('rm -rf {}'.format(tmp_dir))

    # return archiver(
    #     mdl_name=mdl_name,
    #     version=version,
    #     ser_file=ser_file,
    #     mdl_file=mdl_file,
    #     hdl_file=hdl_file,
    #     ext_file=ext_file,
    # )

@app.route('/api/v1/models/status', methods=['GET'])
def get_models_status():
    url = "http://localhost:8080/models"
    response = request.get(url)
    models = response.json()['models']
    status = []
    for model in models:
        model_url = f"{url}/{model['modelName']}/{model['modelVersion']}/ready"
        model_status = request.get(model_url).json()
        status.append({'modelName': model['modelName'], 'version': model['modelVersion'], 'status': model_status['status']})
    return jsonify(status)

@app.route('/api/v1/models/list', methods=['GET'])
def list_models():
    output = subprocess.check_output(['torchserve', '--list']).decode('utf-8')
    models = []
    for line in output.strip().split('\n')[2:]:
        parts = line.split()
        models.append({'model_name': parts[0], 'model_version': parts[1], 'url': parts[2]})
    return jsonify(models)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="3520")

#     parser = argparse.ArgumentParser(description='Flask API for PyTorch models')
#     parser.add_argument('--model-name', type=str, help='Name of the model', required=True)
#     parser.add_argument('--model-path', type=str, help='Path to the PyTorch model file', required=True)
#     parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the API to')
#     parser.add_argument('--port', type=int, default=5000, help='Port to bind the API to')
    
#     args = parser.parse_args()

#     model_dir = os.path.join('model_store', args.model_name)

#     if not os.path.exists(model_dir):
#         os.makedirs(model_dir)

#     model_url = 'file://' + args.model_path
#     load_url(model_url, model_dir)
#     model = torch.jit.load(os.path.join(model_dir, 'model.pt'))


# @app.route('/items/<id>', methods=['GET'])
# def get_item(id):
#   item = Item.query.get(id)
#   del item.__dict__['_sa_instance_state']
#   return jsonify(item.__dict__)

# @app.route('/items', methods=['GET'])
# def get_items():
#   items = []
#   for item in db.session.query(Item).all():
#     del item.__dict__['_sa_instance_state']
#     items.append(item.__dict__)
#   return jsonify(items)

# @app.route('/items', methods=['POST'])
# def create_item():
#   body = request.get_json()
#   db.session.add(Item(body['title'], body['content']))
#   db.session.commit()
#   return "item created"

# @app.route('/items/<id>', methods=['PUT'])
# def update_item(id):
#   body = request.get_json()
#   db.session.query(Item).filter_by(id=id).update(
#     dict(title=body['title'], content=body['content']))
#   db.session.commit()
#   return "item updated"

# @app.route('/items/<id>', methods=['DELETE'])
# def delete_item(id):
#   db.session.query(Item).filter_by(id=id).delete()
#   db.session.commit()
#   return "item deleted"