#!/usr/bin/env python
import snowflake.connector
import pandas as pd
import Config as cfg

query="select "
query += "grade_band, "
query += "avg(total_duration_sum)/60 as avg_course_minutes, "
query += "avg(total_interaction_cnt) as avg_course_interactions, "
query += "avg(course_access_cnt) as avg_course_accesses, "
query += "avg(clb_duration_sum)/60 as avg_collab_minutes, "
query += "avg(clb_access_cnt) as avg_collab_accesses "
query += "from( "
query += "select "
query += "scs.class_section_id as course_id, "
query += "sst.person_id, "
query += "scs.grade_points, "
query += "ceil(grade_points,0) as grade_band, "
query += "sum(lca.duration_sum) as total_duration_sum, "
query += "sum(lca.interaction_cnt) as total_interaction_cnt, "
query += "count(lca.ID) as course_access_cnt, "
query += "sum(ca.duration)/1000 as clb_duration_sum, "
query += "count(ca.ID) as clb_access_cnt "
query += "from cdm_sis.student_term_class_section scs "
query += "inner join cdm_sis.student_term sst "
query += "on sst.id = scs.student_term_id "
query += "inner join cdm_sis.class_section sc "
query += "on sc.id = scs.class_section_id "
query += "inner join cdm_map.person mp "
query += "on mp.sis_person_id = sst.person_id "
query += "inner join cdm_map.course mc "
query += "on mc.sis_course_id = scs.class_section_id "
query += "inner join cdm_lms.course_activity lca "
query += "on lca.person_id = mp.lms_person_id "
query += "and lca.course_id = mc.lms_course_id "
query += "inner join cdm_sis.term st "
query += "on st.ID = sst.term_id "
query += "inner join cdm_map.course_room mcr "
query += "on mcr.lms_course_id = lca.course_id "
query += "left join cdm_clb.session cs "
query += "on cs.room_id = mcr.clb_room_id "
query += "left join cdm_clb.attendance ca "
query += "on ca.session_id = cs.id "
query += "and ca.person_id = mp.clb_person_id "
query += "group by "
query += "scs.class_section_id, "
query += "sst.person_id, "
query += "scs.grade_points "
query += ") a "
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
    
finally:
    cs.close()
ctx.close()