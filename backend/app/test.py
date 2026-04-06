from sqlmodel import Session
from db.session import engine
from models.user import User
from core.security import hash_password

with Session(engine) as session:

    user = User(
        username="testuser",
        password_hash=hash_password("password123"),
        name="Test User",
        rank="Constable",
        policestation="Station A",
        subdivision="Sub A",
        cugphno="9999999999"
    )

    session.add(user)
    session.commit()