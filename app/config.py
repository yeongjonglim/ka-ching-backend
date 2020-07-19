# import logging
import os

SECRET_KEY = os.getenv("SECRET_KEY", "ka-ching")
DEBUG = os.getenv("FLASK_ENV") == "DEV"
ENV = os.getenv("FLASK_ENV")
APP_ROOT = os.getenv("APP_ROOT", "/api")
HOST = os.getenv("APP_HOST")
PORT = int(os.getenv("APP_PORT", "3000"))
SQLALCHEMY_TRACK_MODIFICATIONS = False

DB_CONTAINER = os.getenv("APP_DB", "localhost")
POSTGRES = {
    "user": os.getenv("PG_USER", "postgres"),
    "pw": os.getenv("PG_PW", "docker"),
    "host": os.getenv("PG_HOST", DB_CONTAINER),
    "port": os.getenv("PG_PORT", 5432),
    "db": os.getenv("PG_DB", "dev"),
}
DB_URI = "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES


# logging.basicConfig(
#     filename=os.getenv("SERVICE_LOG", "server.log"),
#     level=logging.DEBUG,
#     format="%(levelname)s: %(asctime)s \
#         pid:%(process)s module:%(module)s %(message)s",
#     datefmt="%d/%m/%y %H:%M:%S",
# )
