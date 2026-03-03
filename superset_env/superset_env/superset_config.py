import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'superset.db')}"

SECRET_KEY = "XJ8g8fmk3l0aiY6eGUS6ojs3IK5mn5r6eyhaVmMUL8v3nQ0XceNi3q2I"