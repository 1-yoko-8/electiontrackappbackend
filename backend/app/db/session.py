from sqlmodel import create_engine, Session
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=5,
)

def get_session():
    with Session(engine) as session:  # with ensures proper closing
        yield session                 # generator function - pause & return - if not this no way to exit automatically as the session gets over