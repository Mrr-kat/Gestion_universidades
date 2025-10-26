from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL_BASE_DATOS = "sqlite:///./universidad.db"

motor = create_engine(
    URL_BASE_DATOS, connect_args={"check_same_thread": False}
)
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)

def obtener_bd():
    bd = SesionLocal()
    try:
        yield bd
    finally:
        bd.close()