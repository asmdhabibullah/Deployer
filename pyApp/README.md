# PyApp API Documentation

This documentation provides a detailed explanation and usage guide for a Python Flask API code that manages machine learning models. The API allows users to upload models, create model archives, serve models using TorchServe, and retrieve information about the available models.

## Prerequisites

Before using the Flask API, ensure that the following dependencies are installed:

- Python 3.x
- Flask
- Flask-CORS
- Flask-JSON
- Requests

You can install these dependencies using the following command:

```bash
pip install flask flask-cors flask-json requests
```

## API Endpoints

The Flask API code provides the following endpoints:

### 1. Upload and Create Model

This endpoint allows users to upload a machine learning model and its associated files to create a model archive.

**Endpoint:** `/api/v1/model/create`\
**Method:** `POST`

#### Request Parameters

The request should contain the following form data:

- `mdl_name` (string): The name of the model.
- `version` (string): The version of the model.
- `mdl_file` (file): The serialized model file.
- `ser_file` (file): The serialized file for the model.
- `hdl_file` (file): The handler file for the model.
- `ext_file` (file): An extra file required by the model.

#### Response

- Success: Returns a JSON response with a message indicating that the model has been uploaded and served successfully.
- Error: Returns a JSON response with a list of errors if any required fields are missing or if there is an issue with the upload. The response status code is set to 400 (Bad Request).

### 2. Get All Model Information

This endpoint retrieves information about all the available models.

**Endpoint:** `/api/v1/model`\
**Method:** `GET`

#### Response

- Success: Returns a JSON response with information about all the available models. The response status code is set to 200 (OK).
- Error: Returns a JSON response with a message indicating that no models were found in the storage folder. The response status code is set to 404 (Not Found).

## Usage Guide

To use the Flask API, follow these steps:

1. Run the API script using the following command:

   ```bash
   python <filename.py>
   ```

   Replace `<filename.py>` with the actual filename of the Python script containing the Flask API code.

2. Once the API is running, you can access the endpoints using HTTP requests. You can use tools like cURL, Postman, or libraries in your preferred programming language to interact with the API.

### Uploading and Creating a Model

To upload and create a model, make a POST request to the `/api/v1/model/create` endpoint with the required form data:

- `mdl_name`: The name of the model.
- `version`: The version of the model.
- `mdl_file`: The serialized model file.
- `ser_file`: The serialized file for the model.
- `hdl_file`: The handler file for the model.
- `ext_file`: An extra file required by the model.

Make sure to include all the required form data fields in the request.

If the model is uploaded successfully and all the required fields are provided, the API will create a directory for the model inside the "models" directory. It will save the uploaded files and create a model archive using the TorchServe tool. The model will then be served using TorchServe.

### Retrieving Model Information

To retrieve information about all the available models, make a GET request to the `/api/v1/model` endpoint.

If there are models available in the storage

 folder, the API will return a JSON response containing information about each model, including the model name, model URL, runtime, minimum workers, maximum workers, batch size, status, and health.

If no models are found in the storage folder, the API will return a JSON response with a message indicating the absence of models.