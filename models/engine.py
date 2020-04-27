from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_engine = create_engine('sqlite:///botdb.sqlite', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=db_engine)
db_session = Session()