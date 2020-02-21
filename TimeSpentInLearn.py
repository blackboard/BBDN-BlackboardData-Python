#!/usr/bin/env python
import snowflake.connector
import pandas as pd
import Config as cfg

query = """
select
   lp.last_name,
   lp.first_name,
   lsa.person_id,
   month(first_accessed_time) as month,
   round(sum(duration_sum)/60,0) as duration_minutes
from cdm_lms.session_activity lsa
inner join cdm_lms.person lp
   on lp.id = lsa.person_id
where
   year(first_accessed_time) = 2018
group by
   lp.last_name,
   lp.first_name,
   lsa.person_id,
   month(first_accessed_time)
"""

outfile = "timeSpentInLearn.csv"

ctx = snowflake.connector.connect(
    user=cfg.sfconcfg['user'],
    password=cfg.sfconcfg['password'],
    account=cfg.sfconcfg['account'],
    warehouse=cfg.sfconcfg['warehouse'],
    database=cfg.sfconcfg['database'],
    insecure_mode=cfg.sfconcfg['insecure_mode']
)
cs = ctx.cursor()
try:
    cs.execute(query)

    # Fetch the result set from the cursor and deliver it as the Pandas DataFrame.
    # df = cs.fetch_pandas_all()
    # TODO: fix this later, switched to pd.read_sql as fetch_pandas_all() causes segfault on linux
    df = pd.read_sql(query, ctx)

    print(df.head())

    df.to_csv(outfile, index=cfg.sfconcfg['timeSpentInLearn']['index'])

finally:
    cs.close()
ctx.close()
