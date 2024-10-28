-- Trips with similar origin, destination, and time of day should be grouped together

-- This should be created a view with this group, but I don't know how to get this similarity betwen diferent origins and destinations
-- So I will create a view based on the similar day time

CREATE VIEW view_name AS
SELECT 
    region,
    origin_coord,
    destination_coord,
    datetime,
    datasource,
    CASE 
        WHEN EXTRACT(HOUR FROM datetime) >= 5 AND EXTRACT(HOUR FROM datetime) < 12 THEN 'Morning'
        WHEN EXTRACT(HOUR FROM datetime) >= 12 AND EXTRACT(HOUR FROM datetime) < 17 THEN 'Afternoon'
        WHEN EXTRACT(HOUR FROM datetime) >= 17 AND EXTRACT(HOUR FROM datetime) < 21 THEN 'Evening'
        ELSE 'Night'
    END AS time_of_day
FROM your_table_name;


SELECT time_of_day, COUNT(*) AS count
FROM view_name
GROUP BY time_of_day
ORDER BY count DESC;