from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#DATABASE_URL = "mysql+mysqlconnector://admin_adso:adso_2025*@127.0.0.1:3366/db"
DATABASE_URL = "mysql+mysqlconnector://root:8480@localhost:3306/proyecto5"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
