#!/usr/bin/env python
import snowflake.connector
import pandas as pd
from matplotlib import pyplot as plt
import Config as cfg

query="select "
query += "grade_band, "
query += "round(avg(ns_clean),2) as avg_grade, "
query += "round(avg(total_duration_sum)/60,0) as avg_course_minutes, "
query += "round(avg(total_interaction_cnt),0) as avg_course_interactions, "
query += "round(avg(course_access_cnt),0) as avg_course_accesses, "
query += "round(avg(clb_duration_sum)/60,0) as avg_collab_minutes, "
query += "round(avg(clb_access_cnt),2) as avg_collab_accesses "
query += "from  "
query += "( "
query += "select "
query += "person_course_id, "
query += "course_id, "
query += "person_id, "
query += "sum(duration_sum) as total_duration_sum, "
query += "sum(interaction_cnt) as total_interaction_cnt, "
query += "count(id) as course_access_cnt "
query += "from cdm_lms.course_activity "
query += "group by "
query += "person_course_id, "
query += "course_id, "
query += "person_id "
query += ") lms "
query += "inner join  "
query += "( "
query += "select "
query += "mcr.lms_course_id, "
query += "mp.lms_person_id, "
query += "sum(ca.duration) as clb_duration_sum, "
query += "count(ca.id) as clb_access_cnt "
query += "from cdm_clb.attendance ca "
query += "inner join cdm_clb.session cs "
query += "on ca.session_id = cs.id "
query += "inner join cdm_map.course_room mcr "
query += "on cs.room_id = mcr.clb_room_id "
query += "inner join cdm_map.person mp "
query += "on mp.clb_person_id = ca.person_id "
query += "group by "
query += "mcr.lms_course_id, "
query += "mp.lms_person_id "
query += ") clb "
query += "on clb.lms_course_id = lms.course_id "
query += "and clb.lms_person_id = lms.person_id "
query += "inner join  "
query += "( "
query += "select "
query += "lg.person_course_id as lpc_id, "
query += "lg.normalized_score, "
query += "case  "
query += "when lg.normalized_score > 1 then 1  "
query += "when lg.normalized_score < 0 then 0 "
query += "else lg.normalized_score  "
query += "end as ns_clean, "
query += "ntile(4) over (order by ns_clean) as grade_band "
query += "from cdm_lms.grade lg "
query += "inner join cdm_lms.gradebook lgb "
query += "on lg.gradebook_id = lgb.id "
query += "and lgb.final_grade_ind = 1 "
query += "and deleted_ind = 0 "
query += "where normalized_score is not null "
query += ") grd "
query += "on grd.lpc_id = lms.person_course_id "
query += "group by grade_band "
query += "order by grade_band"
query += ";"

outfile = "activityEqualsSuccess.csv" 

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

    pd.plotting.parallel_coordinates(
        df, 'GRADE_BAND',
        color=('#556270', '#4ECDC4', '#C7F464', '#FF0000'))
    plt.show()
    
finally:
    cs.close()
ctx.close()