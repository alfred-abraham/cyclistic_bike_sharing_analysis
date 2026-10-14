from pathlib import Path
import duckdb
from pglast import parse_sql

ROOT=Path(__file__).parents[1]

def test_postgresql_syntax():
    for name in ['01_create_raw.sql','Table Creation and Data Cleaning.sql','SQL Data Exploration Queries.sql']:
        parse_sql((ROOT/'sql_files'/name).read_text())

def test_weekend_deduplication_and_duration_boundaries():
    db=duckdb.connect()
    db.execute((ROOT/'sql_files/01_create_raw.sql').read_text())
    db.execute("CREATE MACRO TO_CHAR(d,f) AS CASE WHEN f='Month' THEN strftime(d,'%B') ELSE strftime(d,'%A') END")
    rows=[('fri','2023-01-06 12:00','2023-01-06 12:10'),
          ('sat','2023-01-07 12:00','2023-01-07 12:20'),
          ('sat','2023-01-07 12:00','2023-01-07 12:20'),
          ('sun','2023-01-08 12:00','2023-01-08 12:30'),
          ('zero','2023-01-08 12:00','2023-01-08 12:00'),
          ('long','2023-01-08 12:00','2023-01-09 12:01'),
          ('outside','2022-12-31 12:00','2022-12-31 12:10')]
    for key,start,end in rows:
        db.execute("INSERT INTO divvy_trips_raw(ride_id,started_at,ended_at,member_casual) VALUES (?,?,?,'casual')",[key,start,end])
    db.execute((ROOT/'sql_files/Table Creation and Data Cleaning.sql').read_text())
    assert db.execute('SELECT ride_id,day_of_week FROM divvy_trips_clean ORDER BY ride_id').fetchall()==[('fri',5),('sat',6),('sun',7)]
    assert db.execute('SELECT count(*) FROM divvy_trips_clean WHERE day_of_week IN (6,7)').fetchone()[0]==2
    assert db.execute('SELECT sum(ride_length_minutes) FROM divvy_trips_clean').fetchone()[0]==60
    db.close()
