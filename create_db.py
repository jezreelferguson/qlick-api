# create_db.py
from app.database import engine
from app.model.user import Base

Base.metadata.create_all(bind=engine)