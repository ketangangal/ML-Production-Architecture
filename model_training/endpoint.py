from fastapi import FastAPI, Form, Request
from aws_connection.service import FeatureStoreConnection
from data_preprocessing_service.preprocessing import Preprocessing
import joblib
import pickle as pkl
import uvicorn
import numpy as np
import requests
app = FastAPI()

# create global transforms

global encoder
global scaler
global model

def load_model():
    # Take model from s3
    prod_model = r"F:\Production\ML-Production-Architecture\model_training\artifacts\model.pkl"
    with open(prod_model, 'rb') as f:
        model = pkl.load(f)
        f.close()
    return model

def inference_preprocess(query):
    encoder_path = r"F:\Production\ML-Production-Architecture\model_training\inference_objects\encoder.pkl"
    scaler_path = r"F:\Production\ML-Production-Architecture\model_training\inference_objects\scaler.pkl"
    encoder = joblib.load(encoder_path)
    scaler = joblib.load(scaler_path)
    print("object loaded")
    query = encoder.transform(query)
    query = scaler.transform(query)
    return query


@app.get('/')
def invoke():
    return {"Response": "Hello world from Model Endpoint"}


@app.post('/predict')
async def predict(request: Request):
    query = await request.json()
    query = inference_preprocess([query])
    model = load_model()
    result = model.predict(np.array(query))
    data = {"Result": result.tolist()[0]}
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)


