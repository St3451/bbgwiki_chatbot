import yaml
from yaml.loader import SafeLoader


def load_yaml(path: str):
    """
    Load configuration
    """
    with open(path) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config