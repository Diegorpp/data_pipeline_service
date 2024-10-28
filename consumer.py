from src.helper_functions.broker import consume_message
import pandas as pd
import io
from src.db.database import SessionLocal
from src.db.database import TripData
from datetime import datetime
from src.db.crud import create_trips_bulk



# Define a callback function to process each message
def processing(ch, method, properties, body):
    print(f" [x] Received '{body.decode()}'")
    # TODO: Insert the pipeline processing here.

    df = pd.read_csv(io.StringIO(body.decode("utf-8")))
    db = SessionLocal()

    # Generates a list of TripDataModel, in which insert all the data in a single operation.
    trips = [
        TripData(
            datasource=row['datasource'],
            region=row['region'],
            origin_coord=row['origin_coord'], # Convert later for a version with Lat and Lon
            destination_coord=row['destination_coord'], # Convert later for a version with Lat and Lon
            datetime = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
        )
        for _, row in df.iterrows()
    ]
    inserted = create_trips_bulk(db, trips)
    # This should be a log
    print(f'The number os rows inserted on this batch was: {inserted}')
    # Acknowledge the message was processed
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Done")


if __name__ == '__main__':
    consume_message(processing)