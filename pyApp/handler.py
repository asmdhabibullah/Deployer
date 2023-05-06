import os
import psutil
import subprocess
from torch.utils.model_zoo import load_url
from flask_json import  JsonError, json_response
from model_archiver.model_packaging import package_model

def add_model(model_name, version, serialized_file_path, model_file_path, handler_file_path, extra_file_path):
    """
    Adds a new model to TorchServe.
    Args:
        model_name (str): The name of the model.
        version (str): The version of the model.
        serialized_file_path (str): The path to the serialized file of the model.
        model_file_path (str): The path to the model file.
        handler_file_path (str): The path to the handler file.
        extra_file_path (str): The path to the extra file.
    """
    # Check if TorchServe is already running
    if not is_torchserve_running():
        print('TorchServe is not running. Please start TorchServe first.')
        return
    
    # Create the model archive
    archive_dir = os.path.join(os.getcwd(), 'storages', model_name)
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    model_packaging_args = {
        'model_name': model_name,
        'version': version,
        'serialized_file': serialized_file_path,
        'model_file': model_file_path,
        'handler': handler_file_path,
        'extra_files': [extra_file_path],
        'export_path': archive_dir
    }
    package_model(**model_packaging_args)
    
    # Add the new model to TorchServe
    add_model_args = {
        'model_name': model_name,
        'model_path': archive_dir,
        'handler': handler_file_path,
        'extra_files': [extra_file_path],
        'export_path': os.path.join(os.getcwd(), 'model_store')
    }
    cmd = ['torchserve', ' --start', '--model-store', os.path.join(os.getcwd(), 'model_store'), '--models', '{}={}:{}'.format(model_name, archive_dir, handler_file_path)]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print('Error adding model to TorchServe:')
        print(error.decode('utf-8'))
    else:
        print('Model added to TorchServe.')

def is_torchserve_running():
    """
    Checks if TorchServe is already running.
    Returns:
        bool: True if TorchServe is running, False otherwise.
    """
    for proc in psutil.process_iter():
        try:
            if 'torchserve' in proc.name():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def start_torchserve(model_name, model_store_path):
    """
    Starts TorchServe and loads a model archive.
    Args:
        model_name (str): The name of the model.
        model_archive_path (str): The path to the model archive file.
        model_store_path (str): The path to the directory where the model archive will be stored.
    """
    # Start TorchServe
    # Check if TorchServe is running
    if not is_torchserve_running():
        # Start TorchServe and load the model archive
        # start_torchserve(model_name, model_archive_path, model_store_path)
        cmd = ["torchserve", "--start"]
        subprocess.run(cmd, check=True)

        cmd = ["torchserve", "--start", "--model-store", model_store_path, "--models", f"{model_name}={model_name}.mar"]
        subprocess.run(cmd, check=True)

        # Create the model archive
        archiver(model_name, '1.0', '/path/to/serialized_file.pth', '/path/to/model_file.pth', 'handler.py', 'extra_file.txt')
    else:
        print('TorchServe is already running')

    return "Torch server running on for the model of {}".format(model_name)

def archiver(mdl_name="", version="1.0", ser_file="", mdl_file="", hdl_file="", ext_file=""):
    # create a temporary directory to store the model artifacts
    tmp_dir = os.path.join(os.getcwd(), 'storages')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    # download the model file
    mdl_url = 'https://example.com/models/{}.pth'.format(mdl_name)
    mdl_path = os.path.join(tmp_dir, '{}.pth'.format(mdl_name))
    load_url(mdl_url, mdl_path)

    # create a model archive
    archive_dir = os.path.join(os.getcwd(), 'storages', mdl_name)
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    model_packaging_args = {
        'model_name': mdl_name,
        'version': version,
        'serialized_file': ser_file,
        'model_file': mdl_file,
        'handler': hdl_file,
        'extra_files': [ext_file],
        'export_path': archive_dir
    }

    package_model(**model_packaging_args)

    # remove the temporary directory
    # os.system('rm -rf {}'.format(tmp_dir))

    print('Model archive created at {}'.format(archive_dir))
    
    return start_torchserve(mdl_name, archive_dir)

def raise_error(msg):
    raise JsonError(description='Example text.', code=123)


# class ModelStorage:
#     def __init__(self, model_dir):
#         self.model_dir = model_dir
#         if not os.path.exists(self.model_dir):
#             os.makedirs(self.model_dir)

#     def add_model(self, mdl_name, version, ser_file, mdl_file, hdl_file, ext_file):
#         mdl_path = os.path.join(self.model_dir, mdl_name)
#         if not os.path.exists(mdl_path):
#             os.makedirs(mdl_path)

#         archiver(mdl_name, version, ser_file, mdl_file, hdl_file, ext_file)

#     def get_model(self, mdl_name, version):
#         archive_dir = os.path.join(self.model_dir, mdl_name, version)
#         if not os.path.exists(archive_dir):
#             raise ValueError('Model {} version {} not found'.format(mdl_name, version))

#         return archive_dir


#     # def archiver(mdl_name, ser_path, ):
#     #     marc --model-name test1234 --version 1.0 --serialized-file ./densenet161-8d451a50.pth --model-file ./image_classifier/densenet_161/model.py --handler image_classifier --extra-file ./image_classifier/index_to_name.json

#     # def archiver(self, mdl_name, version, ser_file, mdl_file, hdl_file, ext_file):
#     #     parser = argparse.ArgumentParser(description='Flask API for PyTorch models')
#     #     parser.add_argument('--model-name', type=str, help='Name of the model', required=True)
#     #     parser.add_argument('--model-path', type=str, help='Path to the PyTorch model file', required=True)
#     #     parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the API to')
#     #     parser.add_argument('--port', type=int, default=5000, help='Port to bind the API to')
        
#     #     args = parser.parse_args()

#     #     model_dir = os.path.join('model_store', args.model_name)
        
#     #     if not os.path.exists(model_dir):
#     #         os.makedirs(model_dir)

#     #     model_url = 'file://' + args.model_path
#     #     load_url(model_url, model_dir)
#     #     model = torch.jit.load(os.path.join(model_dir, 'model.pt'))


# class ModelHandler(BaseHandler):
#     """
#     A custom model handler implementation.
#     """

#     def __init__(self):
#         self._context = None
#         self.initialized = False

#     def initialize(self, context):
#         """
#         Initialize model. This will be called during model loading time
#         :param context: Initial context contains model server system properties.
#         :return:
#         """
#         self._context = context
#         self.manifest = context.manifest
#         properties = context.system_properties
        
#         model_dir = properties.get('model_dir')
        
#         model_file_path = os.path.join(model_dir, 'trained_model.pth')
#         model_config_path = os.path.join(model_dir, 'trained_model_config.yaml')
        
#         # defining and loading detectron model
#         self.model = lp.Detectron2LayoutModel(model_config_path, model_file_path,
#                                               extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
#                                               label_map = {
#                                                 1: "TextRegion",
#                                                 2: "ImageRegion",
#                                                 3: "TableRegion",
#                                                 4: "MathsRegion",
#                                                 5: "SeparatorRegion",
#                                                 6: "OtherRegion"
#                                               })
        
#         self.initialized = True
        
#     def preprocess(self, data):
#         """
#         Transform raw input into model input data.
#         :param batch: list of raw requests, should match batch size
#         :return: list of preprocessed model input data
#         """
#         # Take the input data and make it inference ready
#         preprocessed_data = data[0].get("data")
#         if preprocessed_data is None:
#             preprocessed_data = data[0].get("body")

#         return preprocessed_data

#     def inference(self, model_input):
#         """
#         Internal inference methods
#         :param model_input: transformed model input data
#         :return: list of inference output in NDArray
#         """
#         # Do some inference call to engine here and return output
#         model_output = self.model.detect(model_input)
#         return model_output

#     def postprocess(self, inference_output):
#         """
#         Return inference result.
#         :param inference_output: list of inference output
#         :return: list of predict results
#         """
#         # Take output from network and post-process to desired format
#         postprocess_output = inference_output
#         return postprocess_output

#     def handle(self, data, context):
#         """
#         Invoke by TorchServe for prediction request.
#         Do pre-processing of data, prediction using model and postprocessing of prediciton output
#         :param data: Input data for prediction
#         :param context: Initial context contains model server system properties.
#         :return: prediction output
#         """
#         if not self.initialized:
#           self.initialized(context)
          
#         model_input = self.preprocess(data)
#         model_output = self.inference(model_input)
#         return self.postprocess(model_output)