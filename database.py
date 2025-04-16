from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#DATABASE_URL = "mysql+mysqlconnector://admin_adso:adso_2025*@127.0.0.1:3366/db"
#DATABASE_URL = "mysql+mysqlconnector://root:8480@localhost:3306/proyecto5"
#DATABASE_URL = "mysql+mysqlconnector://root:CkoZOLKhfndrYazbNpJKatdJAFukzGuO@interchange.proxy.rlwy.net:14289/dbRailway"

DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_HOST = os.getenv("MYSQLHOST")
DB_PORT = os.getenv("MYSQLPORT")
DB_NAME = os.getenv("MYSQLDATABASE")
print(DB_USER)
credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
print(credentials_json)
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
