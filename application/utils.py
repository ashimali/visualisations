import csv
import os

from flask import current_app


def load_data(filename, encoding="utf-8"):
    path = os.path.join(current_app.config["PROJECT_ROOT"], "data", filename)
    with open(path, encoding=encoding) as f:
        return list(csv.DictReader(f))
