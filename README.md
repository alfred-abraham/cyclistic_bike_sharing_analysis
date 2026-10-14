# Cyclistic Bike-Share Analysis

## Overview

A SQL and Excel analysis of bike-share usage that compares annual members with casual riders and develops membership recommendations.

## Objective

Answer: **How do annual members and casual riders use Cyclistic bikes differently?** Use those differences to suggest ways to convert casual riders into annual members.

## Data

The analysis uses 12 monthly Divvy / Cyclistic trip CSVs covering one year and more than five million rides. Fields include ride identifiers, bike types, timestamps, stations, coordinates, and membership status. The source CSVs are not included in this repository.

## Approach

1. Combine monthly trip files in PostgreSQL.
2. Remove records with missing timestamps or end times that do not follow start times.
3. Derive ride duration, month, and weekday fields.
4. Aggregate trips by month, weekday/weekend, hour, bike type, and rider category.
5. Export query results to Excel for PivotTables and PivotCharts.

See the [cleaning script](sql_files/Table%20Creation%20and%20Data%20Cleaning.sql) and [analysis queries](sql_files/SQL%20Data%20Exploration%20Queries.sql) for the implementation.

## Results

- Member trips peaked in August; casual trips peaked in July.
- Casual riders made a higher proportion of weekend trips and consistently took longer rides.
- Members showed morning (7–9 AM) and evening (4–6 PM) peaks, suggesting commuting.
- Casual usage increased more gradually and peaked later in the day, suggesting recreation.
- Bike-type proportions were similar across the two groups.

These patterns support testing seasonal or weekend membership options and marketing recreational benefits to frequent casual riders.

### Monthly Trip Trends

![Monthly trips by rider category](visuals/Monthly%20Trips.png)

### Weekend and Weekday Usage

![Weekend and weekday trips by rider category](visuals/Weekend%20Weekday%20Graph.png)

### Average Ride Length

![Average ride length by rider category](visuals/Average%20Ride%20Length.png)

### Hourly Trip Patterns

![Hourly trips by rider category](visuals/Hourly%20Trips.png)

More charts are available in [visuals](visuals/). The [case-study presentation](Cyclistic%20Case%20Study.pptx) summarizes the analysis.

## Tools

PostgreSQL, SQL, and Excel PivotTables and PivotCharts.

## How to Run

1. Obtain the 12 monthly trip CSVs used for the case study.
2. Create a PostgreSQL database and run the raw-table creation statement in [the cleaning script](sql_files/Table%20Creation%20and%20Data%20Cleaning.sql).
3. Prepare and import the monthly data into `divvy_trips_raw`, matching its schema. The script expects a `day_of_week` field with Sunday = 1 and Saturday = 7; derive this field if it is absent from the source files.
4. Run the remaining cleaning statements, then the [exploration queries](sql_files/SQL%20Data%20Exploration%20Queries.sql).
5. Export the aggregated results to Excel and create PivotTables and PivotCharts. Sort months using `month_number`.

## Limitations and Next Steps

- Usage patterns suggest motivations but do not establish why individual riders travel.
- Membership recommendations have not been validated through conversion experiments.
- Extensions include station-level analysis, median ride duration, weather effects, and rider retention.

## License

See [LICENSE](LICENSE) for repository licensing. Refer to the dataset source for its usage terms.
