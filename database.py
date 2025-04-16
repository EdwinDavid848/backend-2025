from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#DATABASE_URL = "mysql+mysqlconnector://root:Mondangi707@localhost:3306/prueba_cuatro"
#DATABASE_URL = 'mysql+mysqlconnector://admin_seven:unknown-707@127.0.0.1:3306/db'
DATABASE_URL = "mysql+mysqlconnector://root:iImPBxAlLBXBfwTYmYwSPoxVLbAfdrwy@mainline.proxy.rlwy.net:17609/dbRailway"
#DATABASE_URL = "mysql+mysqlconnector://root:iImPBxAlLBXBfwTYmYwSPoxVLbAfdrwy@mysql.railway.internal:3306/dbRailway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

