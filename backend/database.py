from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the database URL for SQLite.
# The database will be created in the root of the project directory.
# The "check_same_thread" argument is needed only for SQLite. It's required
# because FastAPI can use multiple threads for a single request, and SQLite
# by default doesn't allow this.
SQLALCHEMY_DATABASE_URL = "sqlite:///./agri_loop.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Each instance of the SessionLocal class will be a database session.
# The class itself is not a session yet, but will create one when instantiated.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models.
# All our database models will inherit from this class.
Base = declarative_base()
