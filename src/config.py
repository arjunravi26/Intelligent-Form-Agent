import yaml

CONFIG_PATH = "config.yaml"


def read_config(key: str):
    try:
        if key is None:
            return None
        with open(file=CONFIG_PATH, mode='r') as file:
            config = yaml.safe_load(file)
        return config[key]
    except Exception as e:
        print(f"Raised exception {e}")
        return None


if __name__ == "__main__":
    print(read_config("data_path"))
