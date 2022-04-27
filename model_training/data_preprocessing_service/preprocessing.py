import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from category_encoders import OneHotEncoder
import joblib
# Future Implementation
"""
1. Implementation of joblib 
2. 
"""
class Preprocessing:
    def __init__(self, df: DataFrame, label: str, test_size: int, random_state: int):
        self.df = df
        self.X = self.df.drop([label], axis=1)
        self.y = self.df[label]
        self.test_size = test_size
        self.random_state = random_state

    def __drop_null(self):
        self.df = self.df.dropna()

    def __one_hot_encoding(self,columns:list):
        path = r"F:\Production\ML-Production-Architecture\model_training\inference_objects\encoder.pkl"
        encodings = OneHotEncoder(cols=columns,use_cat_names=True)
        encodings.fit(self.X)
        self.X = encodings.transform(self.X)
        joblib.dump(encodings,path)

    def __train_test_split(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y,
                                                            test_size=self.test_size,
                                                            random_state=self.random_state)
        return X_train, X_test, y_train, y_test

    @staticmethod
    def __feature_scaling(X_train,X_test):
        path = r"F:\Production\ML-Production-Architecture\model_training\inference_objects\scaler.pkl"
        scaler = MinMaxScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        joblib.dump(scaler, path)
        return X_train, X_test

    def preprocess(self):
        self.__drop_null()
        print(self.X.select_dtypes(include=['object']).columns.tolist())
        self.__one_hot_encoding(self.X.select_dtypes(include=['object']).columns.tolist())
        print(self.X.columns.__len__())
        X_train, X_test, y_train, y_test = self.__train_test_split()
        X_train, X_test = self.__feature_scaling(X_train, X_test)
        return X_train, X_test, y_train, y_test

class InferencePreprocessing:
    def __init__(self,query: dict):
        pass

    def load_model(self):
        pass

    def load_encoder(self):
        pass

    def load_scaler(self):
        pass
