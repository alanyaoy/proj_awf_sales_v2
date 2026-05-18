

# this acts as my application's settings parser,securely reading variables out of the system environment



import os
import urllib.parse
from dotenv import load_dotenv

#search for and parse the local .env file
load_dotenv()

class Config:
    """ Central configuration class parsing system environment credentials """
    _server = os.getenv('DB_SERVER')
    _database = os.getenv('DB_NAME')
    _user = os.getenv('DB_USER')
    _password= os.getenv('DB_PASS')
    _sqltbl= os.getenv('SQL_TBL_NAME')
    _csvpath = os.getenv('CSV_PATH')

    # New: Pull an optional sheet name from .env, defaulting to 'Sheet1' if missing
    _sheetname = os.getenv('excel_sheet_name', 'Sheet1')



    #Safely escape specialized password Symbols (@, #, !, etc. ) for SQLAlchemy
    _escaped_params = urllib.parse.quote_plus(
        f"DRIVER={{ ODBC Driver 17 for SQL SERVER}};"
        f"SERVER = {_server};"
        f"DATABASE={_database};"
        #f"UID={_user};"
        #f"PWD={_password};"
        #"ENCRYPT=yes;"
        #"TrustServerCertificate=yes;"
        "Trusted_connections=yes;"
    )

    #Global public endpoint utilized by main.py execution block
    DB_URL = f"mssql+pyodbc:///odbc_connect={_escaped_params}"
    #FILE_PATH = os.getenv('CSV_PATH')
    #TARGET_TABLE = os.getenv('TARGET_TABEL','my_default_table')
    FILE_PATH = _csvpath
    TARGET_TABLE = _sqltbl

    SHEET_NAME =_sheetname          #Clean variable entry point