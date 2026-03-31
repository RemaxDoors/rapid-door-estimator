import urllib
from sqlalchemy import create_engine
from config import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD, DB_DRIVER, validate_config


def get_engine():
    validate_config()

    params = urllib.parse.quote_plus(
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "TrustServerCertificate=yes;"
    )

    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    return engine


