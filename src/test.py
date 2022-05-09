from aws_feature_store.feature_store import FeatureStoreConnection
from exception.exception import CustomException
from app_logging.logging import CustomLogger
from aws_model_registry.model_registry import ModelRegistryConnection
from data_preprocessing_service.inference_loader import ObjectLoader
from email_notification_service.email_service import EmailSender
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, recall_score
from utils.utils import read_config
import requests
import sys
logger = CustomLogger("logs")


class ModelTest:
    def __init__(self):
        self.config = read_config()
        self.feature_store = self.config["feature_store"]["bucket_name"]
        self.raw_data_key = self.config["feature_store"]["file_name"]
        self.model_registry = self.config["model_registry"]["bucket_name"]
        self.zip_files = self.config["model_registry"]["zip_files"]
        self.package_name = self.config["model_registry"]["package_name"]
        self.label = self.config["ml_params"]["label"]
        self.test_size = self.config["ml_params"]["test_size"]
        self.random_state = self.config["ml_params"]["random_state"]
        self.model_endpoint = "https://a00f2d17e0d0.in.ngrok.io/reload"

    def send_email(self):
        mail = EmailSender(sender_email=self.config["email_params"]["sender_email"],
                           application_key=self.config["email_params"]["application_key"],
                           receiver_email=self.config["email_params"]["receiver_email"],
                           message=self.config["email_params"]["test_message"])
        mail.send_email()

    def additional_preprocess(self, raw_Data):
        X = raw_Data.drop(self.label, axis=1)
        y = raw_Data[self.label]
        _, X_test, _, y_test = train_test_split(X, y, test_size=self.config["ml_params"]["test_size"],
                                                random_state=self.config["ml_params"]["random_state"])
        return X_test, y_test

    @staticmethod
    def get_predictions(objects, X_test, y_test):
        encoded = objects["encoder"].transform(X_test)
        scaled = objects["scaler"].transform(encoded)
        prediction = objects["model"].predict(scaled)

        accuracy = accuracy_score(y_test, prediction)
        f1 = f1_score(y_test, prediction)
        recall = recall_score(y_test, prediction)

        return accuracy, f1, recall

    def test(self):
        try:
            feature_data = FeatureStoreConnection(bucket_name=self.feature_store, key=self.raw_data_key)
            registry = ModelRegistryConnection(self.model_registry, self.zip_files, self.package_name)
            loader = ObjectLoader()
            raw_data = feature_data.get_features_from_s3()
            X_test, y_test = self.additional_preprocess(raw_data)

            registry.get_package_from_testing()
            test_objects = loader.load_objects()
            _, f1_test, _ = self.get_predictions(test_objects, X_test, y_test)
            print(f"Testing objects loaded {test_objects}")

            registry.get_package_from_prod()
            prod_objects = loader.load_objects()
            _, f1_prod, _ = self.get_predictions(prod_objects, X_test, y_test)
            print(f"Production objects loaded {prod_objects}")

            print("checking condition")
            print(f"F1 Score Test {f1_test}")
            print(f"F1 Score Prod {f1_prod}")

            if f1_test > f1_prod:
                response = registry.move_model_test_to_prod()
                reload = requests.get(self.model_endpoint)
                print(reload.text)
                print(response)
            else:
                print("Prod model is More accurate")

            return True
        except Exception as e:
            message = CustomException(e, sys)
            logger.error(message.error_message)


if __name__ == "__main__":
    model_selector = ModelTest()
    result = model_selector.test()
    print(result)
