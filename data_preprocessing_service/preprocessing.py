import os
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from category_encoders import OneHotEncoder
import joblib
from from_root import from_root


class Preprocessing:
    def __init__(self, df: DataFrame, label: str, test_size: int, random_state: int):
        self.df = df
        self.X = self.df.drop([label], axis=1)
        self.y = self.df[label]
        self.test_size = test_size
        self.random_state = random_state
        self.encoder = OneHotEncoder(cols=self.X.select_dtypes(include=['object']).columns.tolist(),
                                     use_cat_names=True)
        self.scaler = MinMaxScaler()
        self.encoder_path = os.path.join(from_root(),"artifacts","encoder.pkl")
        self.scaler_path = os.path.join(from_root(),"artifacts","scaler.pkl")

    def __drop_null(self):
        self.df = self.df.dropna()

    def __one_hot_encoding(self):
        self.encoder.fit(self.X)
        self.X = self.encoder.transform(self.X)
        joblib.dump(self.encoder,self.encoder_path)

    def __train_test_split(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y,
                                                            test_size=self.test_size,
                                                            random_state=self.random_state)
        return X_train, X_test, y_train, y_test

    def __feature_scaling(self,X_train,X_test):
        self.scaler.fit(X_train)
        X_train = self.scaler.transform(X_train)
        X_test = self.scaler.transform(X_test)
        joblib.dump(self.scaler, self.scaler_path)
        return X_train, X_test

    def preprocess(self):
        self.__drop_null()
        self.__one_hot_encoding()
        X_train, X_test, y_train, y_test = self.__train_test_split()
        X_train, X_test = self.__feature_scaling(X_train, X_test)
        print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
        return X_train, X_test, y_train, y_test

