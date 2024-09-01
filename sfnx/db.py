from sqlmodel import SQLModel, create_engine, Session, select, Field, UniqueConstraint
from sfnx.security import derive_key, encrypt, decrypt
from sqlalchemy.sql import func
from sqlmodel import SQLModel, Field
from typing import Optional
import os
import sys

db_file = "sfnx.db"
db_url = f"sqlite:///{db_file}"

engine = create_engine(db_url, echo=False)

def init_db():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Error initializing the database: {e}")
        sys.exit(1)

class Secrets(SQLModel, table=True):
    service: str = Field(nullable=False, max_length=64, primary_key=True)
    username: str = Field(nullable=False, max_length=64, primary_key=True)
    password: bytes = Field(nullable=False, max_length=255)
    salt: bytes = Field(nullable=False)

def configure(master_password: str, verification_secret: str) -> bytes:
    try:
        init_db()
        salt = os.urandom(16)
        reference = encrypt(derive_key(master_password, salt), verification_secret)
        configuration = Secrets(
            service="sfnx_secret",
            username=verification_secret,
            password=reference,
            salt=salt
        )
        with Session(engine) as session:
            session.add(configuration)
            session.commit()
    except Exception as e:
        print(f"Error during configuration: {e}")
        sys.exit(1)

def check_exists() -> bool:
    try:
        with Session(engine) as session:
            statement = select(Secrets).where(Secrets.service == "sfnx_secret")
            result = session.exec(statement).first()
            return result is not None
    except Exception as e:
        print(f"Error checking existence: {e}")
        return False

def check_db_exists():
    db_path = "sfnx.db"
    return os.path.isfile(db_path)

def verify_user_master_password(master_password_attempt: str) -> bool:
    try:
        with Session(engine) as session:
            statement = select(Secrets).where(Secrets.service == "sfnx_secret")
            result = session.exec(statement).first()

            if result is None:
                return False
            
            encrypted_secret = getattr(result, "password")
            verification_secret = getattr(result, "username")
            salt = getattr(result, "salt")
            key = derive_key(master_password_attempt, salt)
            try:
                decrypted_secret = decrypt(key, encrypted_secret)
            except ValueError:
                print("Wrong master password.")
                return False

            return decrypted_secret == verification_secret
    except Exception as e:
        print(f"Error verifying master password: {e}")
        return False

def get_user_name(master_password_attempt: str) -> str:
    try:
        with Session(engine) as session:
            if check_exists():
                statement = select(Secrets).where(Secrets.service == "sfnx_secret")
                result = session.exec(statement).first()
                
                verification_secret = getattr(result, "username")
                encrypted_secret = getattr(result, "password")
                salt = getattr(result, "salt")
                key = derive_key(master_password_attempt, salt)

                try:
                    decrypted_secret = decrypt(key, encrypted_secret)
                except ValueError:
                    return ""
                
                if decrypted_secret == verification_secret:
                    return decrypted_secret
                else:
                    return ""
    except Exception as e:
        print(f"Error retrieving user name: {e}")
        return ""

def check_if_service_and_uname_already_exist(service: str, username: Optional[str]) -> bool:
    try:
        with Session(engine) as session:
            statement = select(Secrets).where(Secrets.username == username).where(Secrets.service == service)
            result = session.exec(statement).first()
            return result is not None
    except Exception as e:
        print(f"Error checking service and username existence: {e}")
        return False

def add_password(master_password_attempt: str, service: str, username: Optional[str], password: str):
    try:
        if verify_user_master_password(master_password_attempt) and not service == "sfnx_secret":
            with Session(engine) as session:
                if not check_if_service_and_uname_already_exist(service, username):
                    salt = os.urandom(16)
                    key = derive_key(master_password_attempt, salt)
                    s_password = encrypt(key, password)
                    secret = Secrets(
                        service=service,
                        username=username,
                        password=s_password,
                        salt=salt
                    )
                    session.add(secret)
                    session.commit()
                    print("Password added successfully!")
                else:
                    print("Secrets associated with the same service and username already exist.")
                    return
    except Exception as e:
        print(f"Error adding password: {e}")

def delete_password(master_password_attempt: str, service: str, username: str):
    try:
        if verify_user_master_password(master_password_attempt):
            with Session(engine) as session:
                statement = select(Secrets).where(Secrets.service == service).where(Secrets.username == username)
                result = session.exec(statement).first()
                if result:
                    session.delete(result)
                    session.commit()
                    print("Password deleted successfully!")
    except Exception as e:
        print(f"Error deleting password: {e}")

def retrieve_password(master_password_attempt: str, service: str, username: str):
    try:
        if verify_user_master_password(master_password_attempt):
            with Session(engine) as session:
                statement = select(Secrets).where(Secrets.service == service).where(Secrets.username == username)
                results = session.exec(statement).all()

                if results:
                    for result in results:
                        username = result.username
                        key = derive_key(master_password_attempt, result.salt)
                        try:
                            password = decrypt(key, result.password)
                        except ValueError:
                            password = None

                        return password
                else:
                    return None
    except Exception as e:
        print(f"Error retrieving password: {e}")