# data_pipeline_service
An aplication that provides an API to ingest data on a on-demand basis.

## Requirements for this project.

    Docker

## Setting the environment

The best way to run this project it's through Docker, in which you can set everything up using the docker-compose command bellow:

    docker compose up -d

Then you must access the local url to see the API interface.

    localhost:8000

To manually test it you can click on the endpoint, then on the "Try it out" button. After that um upload the '.csv' file and then click on "Execute".

The CSV file should contain the following columns with this structure:

    datasource: str
    region: str
    origin_coord: POINT (Lat, Lon)
    destination_coord: POINT (Lat, Lon)
    datetime: datetime

## Checklist of things that still need to be done.


[x] - Create the API.

[X] - Create the Postgres Database.

[X] - Integrate the datasbase.

[X] - Create the datamodel and ORM.

[X] - Ingest the simplest data possible.

[ ] - Convert the application to be scalable (Still 
does not suport 100 millions of lines)

[ ] - Create the queries needed for the challenge

[ ] - Convert the database to optimize coordinate data

[ ] - Create some feature to manage the status of the injestion.

[ ] - Create a video to explain the code.

[ ] - Update the last version of the README.md file with all the steps needed to run the project.