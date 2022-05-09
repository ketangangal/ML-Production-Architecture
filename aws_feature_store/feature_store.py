import boto3
import awswrangler as wr


class FeatureStoreConnection:
    """
    This class creates connection with aws and performs
    1. Raw data collection from s3
    2. Raw Data upload to s3
    """
    def __init__(self, bucket_name: str, key: str) -> None:
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

    def upload_features_to_s3(self, df=None) -> str:
        try:
            path_to_s3 = f"s3://{self.bucket_name}/{self.data_key}"
            wr.s3.to_csv(df=df, path=path_to_s3)
            return "File upload successful"
        except Exception as e:
            raise e