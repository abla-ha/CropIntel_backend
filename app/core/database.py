from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# SQLite database URL (for PostgreSQL, use 'postgresql://user:password@localhost/dbname')
SQLALCHEMY_DATABASE_URL = "sqlite:///./cropintel.db"  # Use the appropriate DB URL for your setup

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite-specific setting
)

# Create a SessionLocal class for creating session instances
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for creating models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
