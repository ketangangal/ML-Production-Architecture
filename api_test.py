import requests
from aws_feature_store.feature_store import FeatureStoreConnection

print('request')
response = requests.get("http://localhost:8081/")
print(response.status_code)

feature_data = FeatureStoreConnection(bucket_name="featurestorek10", key="HeartDiseaseTrain-Test.csv")
data = feature_data.get_features_from_s3()
data = data.drop("target",axis=1)
response = requests.post("http://localhost:8081/predict",data=data.iloc[0].to_json())
print(response.text)
print(response.status_code)

