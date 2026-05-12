-- Calculate number of trips per month for both categories of users
SELECT month_name, month_number, member_casual, COUNT(ride_id) as trip_count FROM divvy_trips_clean group by month_name, month_number, member_casual
order by month_number;


-- Calculate the number of trips made by both categories of users on weekends and weekdays
SELECT
    CASE
        WHEN day_of_week IN (1,7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS ride_period,
    member_casual,
    COUNT(*) AS total_trips
FROM divvy_trips_clean
GROUP BY ride_period, member_casual;


-- Calculate average ride length per month for both categories of users 
SELECT month_name, month_number, member_casual, avg(ride_length_minutes) as average_ride_length FROM divvy_trips_clean group by month_name,
month_number, member_casual order by month_number;


-- Calculate number of bikes per category (electric, classic, docked) for both categories of users
SELECT rideable_type, member_casual, COUNT(ride_id) as total_trips FROM divvy_trips_clean group by rideable_type, member_casual;


-- Calculate number of trips per hour of the day for both categories of users
SELECT
    EXTRACT(HOUR FROM started_at) AS ride_hour,
    member_casual,
    COUNT(*) AS trip_count
FROM divvy_trips_clean
GROUP BY ride_hour, member_casual
ORDER BY ride_hour;

