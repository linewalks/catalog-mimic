import pytest
from catalog.config import DB_CFG, REMOTE_DB_CFG
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("catalog-test")

xfail = pytest.mark.xfail


def pytest_generate_tests(metafunc):
    if "db" in metafunc.fixturenames:
        metafunc.parametrize("db", ["local", "remote"], indirect=True)


class DBLocal(object):
    """local database object"""
    def __init__(self):
        if DB_CFG["source_mimic"]:
            self.url = DB_CFG["source_mimic"]
        else:
            self.url = "postgresql://postgres:@127.0.0.1:5432"
        self.engine = create_engine(self.url)
        self.engine.execute("create schema if not exists test")


class DBRemote(object):
    """remote database object"""
    def __init__(self):
        if REMOTE_DB_CFG["source_mimic"]:
            self.url = REMOTE_DB_CFG["source_mimic"]
        else:
            self.url = "postgresql://postgres:@127.0.0.1:5432"
        self.engine = create_engine(self.url)


@pytest.fixture
def db(request):
    if request.param == "local":
        return DBLocal()
    elif request.param == "remote":
        return DBRemote()
    else:
        raise ValueError("invalid internal test config")
