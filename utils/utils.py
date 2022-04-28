import yaml


def read_config(config_path="config.yaml"):
    with open(config_path) as config_file:
        content = yaml.safe_load(config_file)

    return content


if __name__ == "__main__":
    print(read_config())
