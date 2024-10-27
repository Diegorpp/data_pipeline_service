from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL
SQLALCHEMY_DATABASE_URL = "postgresql://engineer_user:my_best_password@db:5432/postgres"

# Create the SQLAlchemy engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL) #, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Model definition
class TripData(Base):
    __tablename__ = "trip_data"
    
    id = Column(Integer, primary_key=True, index=True)
    datasource = Column(String, nullable=False)
    region = Column(String, nullable=False)
    origin_coord = Column(String, nullable=False)
    destination_coord = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)

# Create the database tables
Base.metadata.create_all(bind=engine)
