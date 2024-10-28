import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, File, UploadFile, HTTPException
import io
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

        for chunk in np.array_split(df, 100):  # Splitting data into chunks
            publish_message(chunk.to_csv(index=False))



        # TODO: Write the file in a shared store directory
        
        # TODO: send to the rabbitmq which file has to be read.
        
        # TODO: Create the consumer to read the information from the shared store point

        # TODO: send the message back saindo in which status your request it


        # Return a success message or additional details as needed
        return {"message": "CSV file successfully validated", "columns": df.columns.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")
