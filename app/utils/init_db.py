import logging
from sqlalchemy.orm import Session

from core.config import settings
from app.core.database import SessionLocal, Base, engine
from modules.administrador import crud, schemas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create first superuser
    user = crud.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.AdministradorCreate(
            nombre_completo="Admin User",
            usuario="admin",
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            telefono="1234567890",
        )
        user = crud.create(db, obj_in=user_in)
        logger.info(f"Superuser created: {user.email}")
    else:
        logger.info(f"Superuser already exists: {user.email}")

def main() -> None:
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db)
    logger.info("Initial data created")

if __name__ == "__main__":
    main()
