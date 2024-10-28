-- From the two most commonly appearing regions, which is the latest datasource?

WITH RegionCounts AS (
    SELECT region, COUNT(*) AS region_count
    FROM trip_data
    GROUP BY region
    ORDER BY region_count DESC
    LIMIT 2
),
LatestDatasource AS (
    SELECT t.region, t.datasource, t.datetime,
           RANK() OVER (PARTITION BY t.region ORDER BY t.datetime DESC) AS rank
    FROM trip_data t
    INNER JOIN RegionCounts rc ON t.region = rc.region
)
SELECT region, datasource, datetime
FROM LatestDatasource
WHERE rank = 1;
