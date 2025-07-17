from auth.model import Base
from infrastructure.db.database import engine

Base.metadata.create_all(bind=engine)
