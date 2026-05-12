# Cyclistic Bike-Share Analysis (SQL + Excel)

## Project Overview

This project analyzes one year of Cyclistic bike-share trip data to identify behavioral differences between annual members and casual riders. The primary business objective is to generate recommendations for converting casual riders into annual members.

The project was completed using:

* PostgreSQL for data cleaning, transformation, and querying
* Excel PivotTables and PivotCharts for visualization
* SQL aggregation and time-based analysis for business insights

---

# Business Task

Cyclistic wants to increase the number of annual memberships because members are more profitable long-term than casual riders.

The goal of this analysis is to answer:

> How do annual members and casual riders use Cyclistic bikes differently?

The findings are then used to create data-driven business recommendations aimed at converting casual riders into members.

---

# Dataset

Dataset Source:

* Divvy / Cyclistic historical trip datasets

Files Used:

* 12 monthly CSV files covering one full year of ride activity

Approximate dataset size:

* Over 5 million ride records

Key columns included:

* ride_id
* rideable_type
* started_at
* ended_at
* start_station_name
* end_station_name
* member_casual
* start_lat
* start_lng
* end_lat
* end_lng

Derived columns created during cleaning:

* ride_length_minutes
* month_name
* month_number
* day_of_week
* day_of_week_name
* ride_hour

---

# Tools & Technologies

## PostgreSQL

Used for:

* Combining datasets
* Cleaning data
* Aggregations
* Time-based analysis
* SQL querying

## Excel

Used for:

* PivotTables
* PivotCharts
* Business visualization
* Presentation preparation

---

# Data Cleaning & Preparation

Several preprocessing steps were completed before analysis.

## Cleaning Steps

* Combined all 12 monthly datasets into one PostgreSQL table
* Removed rows with missing timestamps
* Generated ride duration in minutes
* Created month and weekday derived fields
* Created hour-of-day field using SQL date extraction
* Verified chronological sorting using month_number

## Example SQL Transformations

### Create ride duration

```sql
EXTRACT(EPOCH FROM (ended_at - started_at))/60 AS ride_length_minutes
```

### Extract month number

```sql
EXTRACT(MONTH FROM started_at) AS month_number
```

### Extract weekday

```sql
EXTRACT(DOW FROM started_at) AS day_of_week
```

### Extract ride hour

```sql
EXTRACT(HOUR FROM started_at) AS ride_hour
```

---

# Key SQL Queries

## Monthly Trip Trends

```sql
SELECT
    month_name,
    month_number,
    member_casual,
    COUNT(*) AS trip_count
FROM divvy_trips_clean
GROUP BY month_name, month_number, member_casual
ORDER BY month_number;
```

## Trips by Weekend and Weekday

```sql
SELECT
    CASE
        WHEN day_of_week IN (1,7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS ride_period,
    member_casual,
    COUNT(*) AS total_trips
FROM divvy_trips_clean
GROUP BY ride_period, member_casual;
```

## Average Ride Length

```sql
SELECT
    month_name,
    month_number,
    member_casual,
    AVG(ride_length_minutes) AS average_ride_length
FROM divvy_trips_clean
GROUP BY month_name, month_number, member_casual
ORDER BY month_number;
```

## Bike Type Usage

```sql
SELECT
    rideable_type,
    member_casual,
    COUNT(*) AS total_trips
FROM divvy_trips_clean
GROUP BY rideable_type, member_casual;
```

## Hour-of-Day Usage

```sql
SELECT
    EXTRACT(HOUR FROM started_at) AS ride_hour,
    member_casual,
    COUNT(*) AS trip_count
FROM divvy_trips_clean
GROUP BY ride_hour, member_casual
ORDER BY ride_hour;
```

---

# Key Findings

## 1. Strong Seasonal Trends

Both member and casual ridership peak during the summer months and decline during the winter months

However:

* Both members and casual riders have different peaks; the former peak in August while the latter peak in July. 

---

## 2. Casual Riders Ride More on Weekends

Analysis by day of week showed:

* Casual riders make a significantly higher percentage of trips during the weekend

This suggests:

* Casual riders use the bikes more recreationally than members do. 
---

## 3. Casual Riders Take Longer Trips

Average ride duration analysis revealed:

* Casual riders consistently take longer trips than members
* Casual ride lengths peak during summer months
* Member ride durations remain relatively stable year-round

This reinforces the recreational usage pattern among casual riders.

---

## 4. Hour-of-Day Trends Reveal Commuting Patterns

The hour-of-day analysis showed one of the strongest behavioral differences.

### Members

Members exhibit:

* Morning peaks around 7–9 AM
* Large evening peaks around 4–6 PM

This strongly suggests commuter behavior.

### Casual Riders

Casual riders:

* Increase more gradually throughout the day
* Peak later in the afternoon/evening
* Show flatter usage patterns overall

This suggests leisure and recreational usage.

---

## 5. Bike Type Usage Was Similar

Both rider groups used:

* classic bikes
* electric bikes

in relatively similar proportions.

Bike type differences were less strategically useful than behavioral timing differences.

---

# Business Recommendations

Based on the findings, the following recommendations were proposed:

## 1. Introduce Weekend Membership Options

Casual riders heavily use bikes during weekends.

Cyclistic could introduce:

* weekend-only memberships
* flexible short-term plans
* seasonal subscriptions

---

## 2. Target Frequent Casual Riders

Use app/email campaigns to target riders who:

* repeatedly rent during weekends
* take longer rides
* frequently use the same stations

These riders are likely strong membership conversion candidates.

---

## 3. Emphasize Recreational Benefits in Marketing

Marketing for casual riders should focus on:

* leisure riding
* recreation
* tourism
* summer activities

rather than commuter-focused messaging.

---

## 4. Introduce Seasonal Passes

Because casual ridership spikes heavily during warmer months, Cyclistic could offer:

* summer memberships
* 3–4 month seasonal passes
* discounted warm-weather plans

---

# Challenges Encountered

Several technical and analytical challenges were encountered during the project:

* Importing and combining large CSV datasets
* Handling inconsistent column structures
* Cleaning null timestamp values
* Managing chronological month sorting in Excel PivotCharts
* Exporting SQL query results for visualization
* Understanding how Excel handles text-based date categories

These challenges provided valuable experience in:

* ETL workflows
* data cleaning
* SQL aggregation
* business intelligence visualization

---

# Skills Demonstrated

This project demonstrates:

## SQL Skills

* GROUP BY
* ORDER BY
* Aggregate functions
* Date/time extraction
* CASE logic
* Data cleaning
* Multi-file dataset integration

## Data Analysis Skills

* Behavioral segmentation
* Trend analysis
* Time-series analysis
* Business recommendation generation

## Visualization Skills

* PivotTables
* PivotCharts
* Data storytelling
* Business presentation design

---

# Conclusion

This analysis identified clear behavioral differences between annual members and casual riders.

Members primarily exhibit commuter-oriented usage patterns:

* weekday riding
* rush-hour peaks
* shorter, consistent trips

Casual riders exhibit more recreational behavior:

* weekend riding
* longer rides
* strong seasonality
* afternoon/evening usage peaks

These insights support targeted marketing and membership strategies designed to convert casual riders into long-term annual members.

---

# Future Improvements

Potential future enhancements include:

* Geographic station analysis
* Interactive dashboards in Power BI or Tableau
* Predictive modeling for membership conversion
* Median ride duration analysis
* Weather-based ride analysis
* Rider retention analysis

---

# Author

Alfred Abraham

