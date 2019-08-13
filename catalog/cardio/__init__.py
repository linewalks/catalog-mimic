from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from catalog import __DB_URI__

if __DB_URI__:
  engine = create_engine(__DB_URI__)

Session = sessionmaker(bind=engine)

Base = declarative_base()


@contextmanager
def session_scope():
  """Provide a transactional scope around a series of operations."""
  session = Session()
  try:
    yield session
    session.commit()
  except Exception:
    session.rollback()
    raise
  finally:
    session.close()
