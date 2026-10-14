CREATE TABLE divvy_trips_raw (
ride_id TEXT, rideable_type TEXT, started_at TIMESTAMP, ended_at TIMESTAMP,
start_station_name TEXT, start_station_id TEXT, end_station_name TEXT, end_station_id TEXT,
start_lat DOUBLE PRECISION, start_lng DOUBLE PRECISION, end_lat DOUBLE PRECISION, end_lng DOUBLE PRECISION, member_casual TEXT
);
