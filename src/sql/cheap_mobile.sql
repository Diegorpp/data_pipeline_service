-- What regions has the "cheap_mobile" datasource appeared in?

SELECT DISTINCT region
FROM trip_data
WHERE datasource = 'cheap_mobile';
