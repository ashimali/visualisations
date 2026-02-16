# -*- coding: utf-8 -*-
import os
from pathlib import Path


class Config(object):
    APP_ROOT = Path(__file__).parent.resolve()
    PROJECT_ROOT = APP_ROOT.parent.resolve()
    SECRET_KEY = os.environ["SECRET_KEY"]


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestConfig(Config):
    TESTING = True
