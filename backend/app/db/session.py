from sqlmodel import create_engine, Session
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_size=20,        # connections kept ready
    max_overflow=40,     # extra burst capacity
    pool_timeout=30,
    pool_recycle=1800,
)

def get_session():
    with Session(engine) as session:  # with ensures proper closing
        yield session                 # generator function - pause & return - if not this no way to exit automatically as the session gets over