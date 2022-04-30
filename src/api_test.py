from aws_feature_store.feature_store import FeatureStoreConnection
from utils.utils import read_config
import requests


class ApiTest:
    def __init__(self):
        self.config = read_config()
        self.feature_store = self.config["feature_store"]["bucket_name"]
        self.raw_data_key = self.config["feature_store"]["file_name"]
        self.label = self.config["ml_params"]["label"]
        store = FeatureStoreConnection(self.feature_store,self.raw_data_key)
        self.raw_data= store.get_features_from_s3().drop(self.label,axis=1)
        self.endpoint = "http://localhost:8081/"

    def invoke(self):
        response = requests.get(self.endpoint)
        print(response.text)

    def predict(self):
        response = requests.post(self.endpoint + "predict",self.raw_data.iloc[5].to_json())
        print(response.text)

    def reload(self):
        response = requests.get(self.endpoint+"reload")
        print(response.text)


if __name__ == "__main__":
    test = ApiTest()
    test.invoke()
    test.predict()
    test.reload()


