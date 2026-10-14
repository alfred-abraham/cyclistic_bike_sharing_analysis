from pathlib import Path
import concurrent.futures, hashlib, json, urllib.request, zipfile
import duckdb
ROOT=Path(__file__).parent
DATA=ROOT/'data'; DATA.mkdir(exist_ok=True)
def download(month):
    filename=f'2023{month:02}-divvy-tripdata.zip'
    url='https://divvy-tripdata.s3.amazonaws.com/'+filename
    archive=DATA/filename
    if not archive.exists():
        urllib.request.urlretrieve(url,archive)
    with zipfile.ZipFile(archive) as z:
        names=[n for n in z.namelist() if n.endswith('.csv') and not n.startswith('__MACOSX')]
        if len(names)!=1: raise ValueError(names)
        target=DATA/f'2023{month:02}-divvy-tripdata.csv'
        if not target.exists():
            with z.open(names[0]) as source, target.open('wb') as dest:
                import shutil
                shutil.copyfileobj(source,dest)
    print('Downloaded',filename,flush=True)
    return {'month':month,'url':url,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
def run():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        manifest=list(pool.map(download,range(1,13)))
    output=ROOT/'results'; output.mkdir(exist_ok=True)
    db=duckdb.connect(str(DATA/'analysis.duckdb'))
    db.execute("SET memory_limit='1GB'")
    db.execute("SET threads=2")
    db.execute("DROP TABLE IF EXISTS divvy_trips_raw")
    db.execute("DROP TABLE IF EXISTS divvy_trips_clean")
    db.execute((ROOT/'sql_files'/'01_create_raw.sql').read_text())
    for month in range(1,13):
        p=str(DATA/f'2023{month:02}-divvy-tripdata.csv').replace("'","''")
        db.execute(f"INSERT INTO divvy_trips_raw BY NAME SELECT * FROM read_csv('{p}',header=true)")
    # DuckDB-only adapter for PostgreSQL TO_CHAR; the committed SQL otherwise runs unchanged.
    db.execute("CREATE OR REPLACE MACRO TO_CHAR(d,f) AS CASE WHEN f='Month' THEN strftime(d,'%B') ELSE strftime(d,'%A') END")
    sql=(ROOT/'sql_files'/'Table Creation and Data Cleaning.sql').read_text()
    db.execute(sql)
    summary=db.execute("""SELECT member_casual, COUNT(*) AS trips,
    100.0*SUM(CASE WHEN day_of_week IN (6,7) THEN 1 ELSE 0 END)/COUNT(*) AS weekend_percent,
    AVG(ride_length_minutes) AS mean_minutes,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ride_length_minutes) AS median_minutes
    FROM divvy_trips_clean GROUP BY member_casual ORDER BY member_casual""").df()
    summary.to_csv(output/'rider_summary.csv',index=False)
    for name,query in {
    'monthly':"SELECT month_number, member_casual, count(*) trips FROM divvy_trips_clean GROUP BY 1,2 ORDER BY 1,2",
    'hourly':"SELECT ride_hour,member_casual,count(*) trips FROM divvy_trips_clean GROUP BY 1,2 ORDER BY 1,2",
    'bike_types':"SELECT rideable_type,member_casual,count(*) trips FROM divvy_trips_clean GROUP BY 1,2 ORDER BY 1,2",
    'duration':"SELECT month_number,member_casual,avg(ride_length_minutes) mean_minutes,median(ride_length_minutes) median_minutes FROM divvy_trips_clean GROUP BY 1,2 ORDER BY 1,2",
    'weekend':"SELECT CASE WHEN day_of_week IN (6,7) THEN 'Weekend' ELSE 'Weekday' END period,member_casual,count(*) trips FROM divvy_trips_clean GROUP BY 1,2 ORDER BY 1,2"
    }.items():
        table=db.execute(query).df(); table.to_csv(output/(name+'.csv'),index=False)
    audit=db.execute("""SELECT count(*) raw_rows, count(distinct ride_id) distinct_ids,
    count(*) FILTER (WHERE started_at IS NULL OR ended_at IS NULL) missing_timestamps,
    count(*) FILTER (WHERE ended_at<=started_at) nonpositive_durations,
    count(*) FILTER (WHERE ended_at-started_at>INTERVAL '24 hours') over_24_hours FROM divvy_trips_raw""").df().iloc[0].to_dict()
    audit={k:int(v) for k,v in audit.items()}
    audit['clean_rows']=db.execute('SELECT count(*) FROM divvy_trips_clean').fetchone()[0]
    audit['period']='2023-01-01 through 2023-12-31'
    audit['engine']='DuckDB; TO_CHAR adapter only; PostgreSQL syntax parsed separately'
    (output/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    (output/'sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
    import matplotlib.pyplot as plt
    def chart(file,index,value,title):
        table=__import__('pandas').read_csv(output/file)
        ax=table.pivot(index=index,columns='member_casual',values=value).plot.bar(figsize=(9,4))
        ax.set_title(title); ax.set_ylabel(value.replace('_',' ')); ax.tick_params(axis='x',rotation=0)
        plt.tight_layout(); plt.savefig(ROOT/'visuals'/(file.replace('.csv','.png')),dpi=140); plt.close()
    chart('monthly.csv','month_number','trips','2023 trips by month')
    chart('hourly.csv','ride_hour','trips','2023 trips by hour')
    chart('duration.csv','month_number','mean_minutes','2023 mean duration (rides up to 24 hours)')
    chart('bike_types.csv','rideable_type','trips','2023 trips by bike type')
    chart('weekend.csv','period','trips','2023 weekday and weekend trips')
    print(audit,summary.to_string(index=False),flush=True)
    db.close()
if __name__=='__main__': run()
