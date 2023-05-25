# Here's the project plan

1. Create a POST API to archive a PyTorch model using torch-model-archiver and store it in to 'storages' folder.
2.  Create a function to check if a TorchServe instance is already running, and if not, start a new one using the torchserve command.
3. Create a function to check if a model is already registered with the TorchServe instance, and if not, register it using the torch-model-archiver command.
4. Modify the POST API to check if TorchServe is already running, and if not, start a new instance. Then register the new model with TorchServe.
5. Create a GET API to retrieve information on all the running models.
6. Create a Flask Rest API app to get access from NextJS Front-End app.

# Objective:
1. This project is designed to avoid having to use a command line interface, as well as how to easily perform can deploy, and run a PyTorch-trained model after storing it in a project folder 'Storages'.

## CMD
1. Create a model runner file with a .mar extention
```
torch-model-archiver --model-name densenet161 \
--version 1.0 \
--model-file ./image_classifier/densenet_161/model.py \
--serialized-file ./densenet161-8d451a50.pth \ 
--extra-files ./image_classifier/index_to_name.json \
--handler ./image_classifier
```
or
```
torch-model-archiver --model-name test1234 --version 1.0 --serialized-file ./densenet161-8d451a50.pth --model-file ./image_classifier/densenet_161/model.py --handler image_classifier --extra-file ./image_classifier/index_to_name.json
```

2. Start a PyTorch server and attach model with the running server
```
torchserve --start --model-store ./test_models --models test1234=./test_models/test1234.mar
```
or
```
torchserve --start --ncs --ts-config ./config.properties --log-config ./config-logs --model-store ./test_models --models test1234=./test_models/test1234.mar
```

# PyApp Implimentatiion & API Documentation

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



# JSApp Frontent doc

## This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

### Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `pages/index.tsx`. The page auto-updates as you edit the file.

[API routes](https://nextjs.org/docs/api-routes/introduction) can be accessed on [http://localhost:3000/api/hello](http://localhost:3000/api/hello). This endpoint can be edited in `pages/api/hello.ts`.

The `pages/api` directory is mapped to `/api/*`. Files in this directory are treated as [API routes](https://nextjs.org/docs/api-routes/introduction) instead of React pages.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.

