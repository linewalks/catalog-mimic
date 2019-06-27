from catalog.config import DB_CFG
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
if DB_CFG["source_mimic"]:
  engine = create_engine(DB_CFG["source_mimic"])
else:
  engine = create_engine("postgresql://postgres:@127.0.0.1:5432")

Session = sessionmaker(bind=engine)

Base = declarative_base()
