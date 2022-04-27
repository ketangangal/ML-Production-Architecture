import os

import boto3
import awswrangler as wr
import pandas as pd
import pickle as pkl
class FeatureStoreConnection:
    """
    This class creates connection with aws and performs
    1. Raw data collection from s3
    2. Raw Data upload to s3
    """
    def __init__(self,bucket_name: str,key: str) -> None:
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket_name
        self.bucket = self.s3.Bucket(bucket_name)
        self.data_key = key

    def get_features_from_s3(self) -> object:
        try:
            path_to_s3 = f"s3://{self.bucket_name}/{self.data_key}"
            df = wr.s3.read_csv(path=path_to_s3)
            return df
        except Exception as e:
            raise e

    def upload_features_from_s3(self,df=None) -> str:
        try:
            path_to_s3 = f"s3://{self.bucket_name}/{self.data_key}"
            wr.s3.to_csv(df=df,path=path_to_s3)
            return "File upload successful"
        except Exception as e:
            raise e


class ModelRegistryConnection:
    def __init__(self,bucket_name: str,testing_key: str,production_key: str):
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket_name
        self.bucket = self.s3.Bucket(bucket_name)
        self.testing_key = f"testing/{testing_key}"
        self.production_key = f"production/{production_key}"

    def upload_model_in_test(self,model: object,path: str):
        """ Pickle object upload in testing"""
        try:
            filehandler = open(path, 'wb')
            pkl.dump(model,filehandler)
            filehandler.close()
            self.s3.meta.client.upload_file(path, self.bucket_name, self.testing_key)
        except Exception as e:
            raise e

    def upload_model_in_prod(self,model: object,path: str):
        """ Pickle object upload in production"""
        try:
            filehandler = open(path, 'wb')
            pkl.dump(model,filehandler)
            filehandler.close()
            self.s3.meta.client.upload_file(path, self.bucket_name, self.production_key)
        except Exception as e:
            raise e

    def get_model_from_testing(self):
        new_model = r'F:\Production\ML-Production-Architecture\model_training\artifacts\newModel.pkl'
        self.bucket.download_file(self.testing_key,new_model)

        while not os.path.exists(new_model):
            pass

        with open(new_model, 'rb') as f:
            model = pkl.load(f)
            f.close()

        return model

    def get_model_from_prod(self):
        prod_model = r'F:\Production\ML-Production-Architecture\model_training\artifacts\prodModel.pkl'
        self.bucket.download_file(self.testing_key,prod_model)

        while not os.path.exists(prod_model):
            pass

        with open(prod_model, 'rb') as f:
            model = pkl.load(f)
            f.close()

        return model

    def move_model_test_to_prod(self):
        """ Model movement from test to prod registry """
        try:
            copy_source = {
                'Bucket': self.bucket_name,
                'Key': self.testing_key
            }
            self.bucket.copy(copy_source,self.production_key)
            return "Model Moved in Production"
        except Exception as e:
            raise e


if __name__ == "__main__":
    feature_Store = FeatureStoreConnection(bucket_name="featurestorek10",
                                           key="HeartDiseaseTrain-Test.csv")

    # Upload file
    df = pd.read_csv(r"F:\downloads\archive\HeartDiseaseTrain-Test.csv")
    response = feature_Store.upload_features_from_s3(df)
    df = feature_Store.get_features_from_s3()
    print(df)