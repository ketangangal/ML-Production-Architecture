from utils.utils import read_config
from aws_model_registry.model_registry import ModelRegistryConnection
from from_root import from_root
from joblib import load
import os


class ObjectLoader:
    def __init__(self):
        self.config = read_config()
        self.extract_folder = os.path.join(from_root(), "artifacts")
        self.files = self.config["model_registry"]["zip_files"]

    def load_objects(self):
        objects = {}
        for obj in self.files:
            path = os.path.join(self.extract_folder, obj)
            objects[obj.replace(".pkl", "")] = load(path)
            os.remove(path)

        return objects


if __name__ == "__main__":
    config = read_config()
    registry = ModelRegistryConnection(config["model_registry"]["bucket_name"],
                                       config["model_registry"]["zip_files"],
                                       config["model_registry"]["package_name"])

    loader = ObjectLoader()
    registry.get_package_from_testing()
    obj = loader.load_objects()
    print(obj)
