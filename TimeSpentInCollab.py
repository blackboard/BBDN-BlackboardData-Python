#!/usr/bin/env python
import snowflake.connector
import pandas as pd
import Config as cfg

query = """
select
  count(distinct room_id) as room_count,
  count(id) as session_count,
  session_count / room_count as avg_sessions_per_room,
  sum(attended_duration/60) as session_minutes_sum
from cdm_clb.session
where attended_duration > 0
"""

outfile = "timeSpentInCollab.csv"

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
    df = cs.fetch_pandas_all()

    print(df.head())

    df.to_csv(outfile, index=False)

finally:
    cs.close()
ctx.close()
