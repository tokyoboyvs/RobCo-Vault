import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / 'instance'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'DEV-ONLY') # Change the DEV-ONLY key for prod.
    DATABASE_PATH = INSTANCE_DIR / 'robco.db'
