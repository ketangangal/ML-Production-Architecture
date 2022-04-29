from aws_model_registry.model_registry import ModelRegistryConnection
from data_preprocessing_service.inference_loader import ObjectLoader
from utils.utils import read_config
from fastapi import FastAPI, Request
import uvicorn


app = FastAPI()

model, encoder, scaler = None, None, None

class PrepareEndpoints:
    def __init__(self):
        self.config = read_config()
        self.model_registry = self.config["model_registry"]["bucket_name"]
        self.zip_files = self.config["model_registry"]["zip_files"]
        self.package_name = self.config["model_registry"]["package_name"]

    def inference_object_loader(self) -> None:
        global encoder
        global scaler
        global model

        registry = ModelRegistryConnection(self.model_registry,
                                           self.zip_files,
                                           self.package_name)
        registry.get_package_from_prod()
        loader = ObjectLoader()
        prod_objects = loader.load_objects()

        encoder = prod_objects["encoder"]
        scaler = prod_objects["scaler"]
        model = prod_objects["model"]


@app.get('/')
def invoke():
    return {"Response": "Hello world from Model Endpoint"}


@app.post('/predict')
async def predict(request: Request):
    query = await request.json()
    encoded = encoder.transform([query])
    scaled = scaler.transform(encoded)
    result = model.predict(scaled)
    result = {"Result": result.tolist()[0]}
    return result

@app.get('/reload')
def reload():
    executor = PrepareEndpoints()
    executor.inference_object_loader()
    return {"Response": "Updating Model In Prod"}


if __name__ == "__main__":
    executor = PrepareEndpoints()
    executor.inference_object_loader()
    uvicorn.run(app, host="localhost", port=8081)
