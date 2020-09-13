import os

this_dir, _ = os.path.split(__file__)


def get_db_absolute_path(db_path: str) -> str:
    abspath = os.path.join(this_dir, "db", db_path)
    return abspath


def get_model_absolute_path(model_path: str) -> str:
    abspath = os.path.join(this_dir, "models", model_path)
    return abspath
