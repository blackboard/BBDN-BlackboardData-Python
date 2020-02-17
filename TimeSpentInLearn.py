#!/usr/bin/env python
import snowflake.connector
import pandas as pd
import Config as cfg

query="select "
query+="lp.last_name, "
query+="lp.first_name, "
query+="lsa.person_id, "
query+="month(first_accessed_time) as month, "
query+="round(sum(duration_sum)/60,0) as duration_minutes "
query+="from cdm_lms.session_activity lsa "
query+="inner join cdm_lms.person lp "
query+="on lp.id = lsa.person_id "
query+="where "
query+="year(first_accessed_time) = 2018 "
query+="group by "
query+="lp.last_name, "
query+="lp.first_name, "
query+="lsa.person_id, "
query+="month(first_accessed_time) "
query += ";"

outfile = "timeSpentInLearn.csv" 

ctx = snowflake.connector.connect(
    user=cfg.sfconcfg['user'],
    password=cfg.sfconcfg['password'],
    account=cfg.sfconcfg['account'],
    warehouse=cfg.sfconcfg['warehouse'],
    database=cfg.sfconcfg['database']
    )
cs = ctx.cursor()
try:
    cs.execute(query)

    # Fetch the result set from the cursor and deliver it as the Pandas DataFrame.
    df = cs.fetch_pandas_all()

    print(df.head())

    df.to_csv(outfile)
    
finally:
    cs.close()
ctx.close()