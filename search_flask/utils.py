import os

this_dir, _ = os.path.split(__file__)


def get_db_absolute_path(db_path: str) -> str:
    abspath = os.path.join(this_dir, "db", db_path)
    return abspath
