__DB_URI__ = None


def initDB(db_uri):
  global __DB_URI__
  if __DB_URI__ is None:
    __DB_URI__ = db_uri
  else:
    raise RuntimeError("Database URI has already been set.")
