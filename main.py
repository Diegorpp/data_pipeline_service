import pandas as pd
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.db.database import SessionLocal
from fastapi import FastAPI, File, UploadFile, HTTPException
import io
from src.db.crud import create_trips_bulk
from src.db.database import TripData
from datetime import datetime
from src.helper_functions.broker import publish_message

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

app = FastAPI()

# Endpoint responsable for receiving a csv file and insert all the data on database
# The insertion in this context is executed in batch
@app.post('/receive_csv_data')
async def upload_csv(file: UploadFile = File(...)):
    # Check file type
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are allowed.")

    # Read the CSV content into a Pandas DataFrame
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))

        # Perform validation on the DataFrame as needed
        # Example: Check if certain columns exist
        required_columns = ['region', 'origin_coord', 'destination_coord', 'datetime', 'datasource']
        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(status_code=400, detail=f"Missing required column: {col}")

        # TODO: Write the file in a shared store directory

        # TODO: send to the rabbitmq which file has to be read.
        publish_message(file.filename)
        
        # TODO: Create the consumer to read the information from the shared store point

        # TODO: send the message back saindo in which status your request it

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


        # Return a success message or additional details as needed
        return {"message": "CSV file successfully validated", "columns": df.columns.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")
