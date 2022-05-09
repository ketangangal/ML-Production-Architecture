from joblib import load, dump
from from_root import from_root
import tarfile
import boto3
import os


class ModelRegistryConnection:
    def __init__(self,bucket_name: str,zip_files: list, package_name: str):
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket_name
        self.bucket = self.s3.Bucket(bucket_name)
        self.zip_files = zip_files
        self.package_name = package_name
        self.zip_file_path = os.path.join(from_root(),"artifacts",f'{self.package_name}.tar.gz')
        self.testing_key = f"testing/{package_name}"
        self.production_key = f"production/{package_name}"

    def upload_model_in_test(self):
        """ Pickle object upload in testing"""
        try:
            folder = tarfile.open(self.zip_file_path, "w:gz")
            print(self.zip_file_path)
            for name in self.zip_files:
                folder.add(os.path.join(from_root(),"artifacts",name),name)
                os.remove(os.path.join(from_root(),"artifacts",name))
            folder.close()

            self.s3.meta.client.upload_file(self.zip_file_path, self.bucket_name, f'{self.testing_key}.tar.gz')
            os.remove(self.zip_file_path)

        except Exception as e:
            raise e

    def upload_model_in_prod(self):
        """ Pickle object upload in production"""
        try:
            folder = tarfile.open(self.zip_file_path, "w:gz")
            print(folder)
            for name in self.zip_files:
                folder.add(os.path.join(from_root(),"artifacts",name),name)
                os.remove(os.path.join(from_root(), "artifacts", name))
            folder.close()

            self.s3.meta.client.upload_file(self.zip_file_path, self.bucket_name, f'{self.production_key}.tar.gz')
            os.remove(self.zip_file_path)
        except Exception as e:
            raise e

    def get_package_from_testing(self):
        zip_file_path = os.path.join(from_root(), "artifacts", f'{self.package_name}.tar.gz')
        self.bucket.download_file(f'{self.testing_key}.tar.gz', zip_file_path)
        folder = tarfile.open(zip_file_path)
        folder.extractall(os.path.join(from_root(), "artifacts"))
        folder.close()
        os.remove(zip_file_path)

    def get_package_from_prod(self):
        zip_file_path = os.path.join(from_root(), "artifacts", f'{self.package_name}.tar.gz')
        self.bucket.download_file(f'{self.production_key}.tar.gz',zip_file_path)
        folder = tarfile.open(zip_file_path)
        folder.extractall(os.path.join(from_root(), "artifacts"))
        folder.close()
        os.remove(zip_file_path)

    def move_model_test_to_prod(self):
        """ Model movement from test to prod registry """
        try:
            copy_source = {
                'Bucket': self.bucket_name,
                'Key': f'{self.testing_key}.tar.gz'
            }
            self.bucket.copy(copy_source,f'{self.production_key}.tar.gz')
            return "Model Moved in Production"
        except Exception as e:
            raise e

