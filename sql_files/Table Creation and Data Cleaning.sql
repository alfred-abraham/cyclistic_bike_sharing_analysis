-- Create table
CREATE TABLE divvy_trips_raw (
    ride_id TEXT,
    rideable_type TEXT,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    start_station_name TEXT,
    start_station_id TEXT,
    end_station_name TEXT,
    end_station_id TEXT,
    start_lat DOUBLE PRECISION,
    start_lng DOUBLE PRECISION,
    end_lat DOUBLE PRECISION,
    end_lng DOUBLE PRECISION,
    member_casual TEXT,
	ride_length TEXT,
	day_of_week INTEGER
	
);
-- Verify that all tables are downloaded properly
SELECT COUNT(*) FROM divvy_trips_raw;

-- Create cleaned version of the table
CREATE TABLE divvy_trips_clean AS
SELECT
    ride_id,
    rideable_type,
    started_at,
    ended_at,
    start_station_name,
    start_station_id,
    end_station_name,
    end_station_id,
    start_lat,
    start_lng,
    end_lat,
    end_lng,
    member_casual,
    day_of_week,

    EXTRACT(EPOCH FROM (ended_at - started_at)) / 60 AS ride_length_minutes,

    EXTRACT(MONTH FROM started_at) AS month_number,
    TO_CHAR(started_at, 'Month') AS month_name,
    TO_CHAR(started_at, 'Day') AS day_of_week_name
FROM divvy_trips_raw
WHERE started_at IS NOT NULL
  AND ended_at IS NOT NULL
  AND ended_at > started_at;
