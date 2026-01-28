from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#engine
DATABASE_URL = "sqlite:////Users/marion/Documents/project/DEKAI CODE/DEKAI.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
#base
Base=declarative_base()

#session
sessionmk=sessionmaker(bind=engine,autoflush=False,autocommit=False)

def get_db():
    db=sessionmk()
    try:
        yield db
    finally:
        db.close()

db=get_db()