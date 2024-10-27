from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from src.db.database import SessionLocal, TripData
from src.db.schemas import TripDataModel

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from typing import List, Optional
def create_trips_bulk(db: Session, trips: List[TripDataModel]):
    """
    Bulk inserts a list of TripData instances into the database.
    
    Parameters:
    - db (Session): SQLAlchemy database session
    - trips (List[TripData]): List of TripData objects to insert
    
    Returns:
    - int: Number of rows inserted
    """
    # Bulk insert the list of TripData instances
    db.bulk_save_objects(trips)
    db.commit()
    
    # Return the number of rows inserted
    return len(trips)


# Create
def create_trip(db: Session, datasource: str, region: str, origin_coord: float, destination_coord: float, datetime: date):
    trip = TripDataModel(
        datasource=datasource,
        region=region,
        origin_coord=origin_coord,
        destination_coord=destination_coord,
        datetime=datetime
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip

# Read single trip by id
def get_trip(db: Session, trip_id: int) -> Optional[TripData]:
    return db.query(TripData).filter(TripData.id == trip_id).first()

# Read multiple trips with optional pagination
def get_trips(db: Session, skip: int = 0, limit: int = 10) -> List[TripData]:
    return db.query(TripData).offset(skip).limit(limit).all()

# Update a trip
def update_trip(db: Session, trip_id: int, datasource: str, region: str, origin_coord: float, destination_coord: float, datetime: date):
    trip = db.query(TripData).filter(TripData.id == trip_id).first()
    if trip:
        trip.datasource = datasource
        trip.region = region
        trip.origin_coord = origin_coord
        trip.destination_coord = destination_coord
        trip.datetime = datetime
        db.commit()
        db.refresh(trip)
    return trip

# Delete a trip
def delete_trip(db: Session, trip_id: int):
    trip = db.query(TripData).filter(TripData.id == trip_id).first()
    if trip:
        db.delete(trip)
        db.commit()
    return trip
