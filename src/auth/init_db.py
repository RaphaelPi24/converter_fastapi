from auth.database import engine
from auth.model import Base

Base.metadata.create_all(bind=engine)
