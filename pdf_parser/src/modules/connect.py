from ..config.settings import get_settings
from contextlib import contextmanager

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, scoped_session

@contextmanager
def get_session_from_engine(engine):
    session = scoped_session(sessionmaker(bind=engine))
    try:
        yield session()
    except Exception as e:
        raise e from None
    finally:
        session.close()

Base = declarative_base()

def create_and_check_engine(database_url, echo=False, pool_size=50, max_overflow=0):
    try:
        engine = create_engine(
            database_url, echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        with engine.connect() as connection:
            print("Connection successful!")   
            return engine
    except Exception as e:
        print(f"Connection failed: {e}")
        return None 