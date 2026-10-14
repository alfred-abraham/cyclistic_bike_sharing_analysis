-- After importing official 13-column CSVs. ISO weekday: Monday=1, Sunday=7.
CREATE TABLE divvy_trips_clean AS
WITH ranked AS (
SELECT *, ROW_NUMBER() OVER (PARTITION BY ride_id ORDER BY started_at, ended_at,
rideable_type, member_casual, start_station_id, end_station_id) AS occurrence
FROM divvy_trips_raw WHERE ride_id IS NOT NULL AND ride_id <> ''
), valid AS (
SELECT * FROM ranked WHERE occurrence=1
AND started_at IS NOT NULL AND ended_at IS NOT NULL
AND started_at >= TIMESTAMP '2023-01-01' AND started_at < TIMESTAMP '2024-01-01'
AND ended_at > started_at AND ended_at-started_at <= INTERVAL '24 hours'
AND member_casual IN ('member','casual')
)
SELECT ride_id, rideable_type, started_at, ended_at, start_station_name,
start_station_id, end_station_name, end_station_id, start_lat, start_lng, end_lat, end_lng, member_casual,
CAST(EXTRACT(ISODOW FROM started_at) AS INTEGER) AS day_of_week,
EXTRACT(EPOCH FROM (ended_at-started_at))/60.0 AS ride_length_minutes,
EXTRACT(MONTH FROM started_at) AS month_number,
TRIM(TO_CHAR(started_at,'Month')) AS month_name,
TRIM(TO_CHAR(started_at,'Day')) AS day_of_week_name,
EXTRACT(HOUR FROM started_at) AS ride_hour FROM valid;
CREATE UNIQUE INDEX divvy_trips_clean_ride_id ON divvy_trips_clean(ride_id);
SELECT COUNT(*) AS raw_rows, COUNT(DISTINCT ride_id) AS distinct_ids FROM divvy_trips_raw;
SELECT COUNT(*) AS clean_rows, MIN(started_at) AS first_trip, MAX(started_at) AS last_trip FROM divvy_trips_clean;
SELECT COUNT(*) AS invalid_duration_rows FROM divvy_trips_raw
WHERE ended_at <= started_at OR ended_at-started_at > INTERVAL '24 hours';
