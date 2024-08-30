from sqlmodel import SQLModel, create_engine, Session, select, Field
from sfnx.security import derive_key, encrypt, decrypt
from sqlmodel import SQLModel, Field
from typing import Optional

db_file = "sfnx.db"
db_url = f"sqlite:///{db_file}"

engine = create_engine(db_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

class Secrets(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, index=True)
    service: str = Field(nullable=False, max_length=64)
    username: Optional[str] = Field(nullable=True, max_length=64)
    password: bytes = Field(nullable=False, max_length=255)

def configure(master_password: str, verification_secret: str) -> bytes:
    reference = encrypt(derive_key(master_password), verification_secret)
    configuration = Secrets(
        service="sfnx_secret",
        username=verification_secret,
        password=reference
    )
    with Session(engine) as session:
        session.add(configuration)

def check_exists() -> bool:
    with Session(engine) as session:
        statement = select(Secrets).where(Secrets.id == 1).where(Secrets.service == "sfnx_secret")
        result = session.exec(statement).first()

        return result is not None

def verify_user_master_password(master_password_attempt: str) -> bool:
    with Session(engine) as session:
        statement = select(Secrets).where(Secrets.id == 1).where(Secrets.service == "sfnx_secret")
        result = session.exec(statement).first()

        if result is None:
            return False
        
        encrypted_secret = getattr(result, "password")
        verification_secret = getattr(result, "username")

        key = derive_key(master_password_attempt)
        decrypted_secret = decrypt(key, encrypted_secret)
        return decrypted_secret == verification_secret
