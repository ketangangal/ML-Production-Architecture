from aws_feature_store.feature_store import FeatureStoreConnection
from aws_model_registry.model_registry import ModelRegistryConnection
from data_preprocessing_service.preprocessing import Preprocessing
from email_notification_service.email_service import EmailSender
from sklearn.metrics import accuracy_score


def unit_test():
    feature_data = FeatureStoreConnection(bucket_name="featurestorek10", key="HeartDiseaseTrain-Test.csv")
    data = feature_data.get_features_from_s3()

    #  Preprocessing on Data
    preprocess = Preprocessing(data, "target", test_size=0.30, random_state=101)
    _, X_test, _, y_test = preprocess.preprocess()

    # Fetch model from s3 testing folder
    registry = ModelRegistryConnection("modelregistryk10", "model.pkl", "model.pkl")
    newModel = registry.get_model_from_testing()
    prodModel = registry.get_model_from_prod()

    new_model_result = newModel.predict(X_test)
    prod_model_result = prodModel.predict(X_test)

    new_model_score = accuracy_score(y_test,new_model_result)
    prod_model_score = accuracy_score(y_test, prod_model_result)

    print("New Model Accuracy", new_model_score)
    print("prod Model Accuracy", prod_model_score)

    if new_model_score > prod_model_score:
        status = registry.move_model_test_to_prod()
    else:
        status = "Production Model Accuracy is More so no movement"
    print(status)
    # Email Notification
    # sender_email = "ketangangal98@gmail.com"
    # receiver_email = "ketangangal98@gmail.com"
    # application_key =
    # message = status
    #
    # mail = EmailSender(sender_email, application_key, receiver_email, message)
    # mail.send_email()
    return True


if __name__ == "__main__":
    response = unit_test()
    print(response)
