# Blackboard Data Python Demos

This project contains three sample scripts to run queries against Blackboard Data, pull them into Pandas Dataframes, and export the data to CSV files. In these samples, we have three queries:

* Time Spent In Learn

```
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
   month(first_accessed_time
```

* Time Spent In Collab

```
select
  count(distinct room_id) as room_count,
  count(id) as session_count,
  session_count / room_count as avg_sessions_per_room,
  sum(attended_duration/60) as session_minutes_sum
from cdm_clb.session
where attended_duration > 0
```

* Activity Equals Success

```
select
  grade_band,
  avg(total_duration_sum)/60 as avg_course_minutes,
  avg(total_interaction_cnt) as avg_course_interactions,
  avg(course_access_cnt) as avg_course_accesses,
  avg(clb_duration_sum)/60 as avg_collab_minutes,
  avg(clb_access_cnt) as avg_collab_accesses
from(
 select
   scs.class_section_id as course_id,
   sst.person_id,
   scs.grade_points,
   ceil(grade_points,0) as grade_band,
   sum(lca.duration_sum) as total_duration_sum,
   sum(lca.interaction_cnt) as total_interaction_cnt,
   count(lca.ID) as course_access_cnt,
   sum(ca.duration)/1000 as clb_duration_sum,
   count(ca.ID) as clb_access_cnt
 from cdm_sis.student_term_class_section scs
   inner join cdm_sis.student_term sst
     on sst.id = scs.student_term_id
   inner join cdm_sis.class_section sc
     on sc.id = scs.class_section_id
   inner join cdm_map.person mp
     on mp.sis_person_id = sst.person_id
   inner join cdm_map.course mc
     on mc.sis_course_id = scs.class_section_id
   inner join cdm_lms.course_activity lca
     on lca.person_id = mp.lms_person_id
     and lca.course_id = mc.lms_course_id
   inner join cdm_sis.term st
     on st.ID = sst.term_id
   inner join cdm_map.course_room mcr
     on mcr.lms_course_id = lca.course_id
   left join cdm_clb.session cs
     on cs.room_id = mcr.clb_room_id
   left join cdm_clb.attendance ca
     on ca.session_id = cs.id
     and ca.person_id = mp.clb_person_id
 group by
   scs.class_section_id,
   sst.person_id,
   scs.grade_points
) a
group by grade_band
order by grade_band
```

## Setting Up Your Environment

This project was built with Python 3.7. Other versions may work, but have not been tested. The project itself requires three Python Libraries:

* Snowflake Python Connector
* Snowflake Python Connecter Pandas Updates
* Pandas

To install the libraries, use `pip`:

```
# Install Snowflake Python Connector

pip install --upgrade snowflake-connector-python

# Install Snowflake Python Connector Pandas Updates 
# Double quotes required on MacOS, not required on windows

pip install "snowflake-connector-python[pandas]"    

# Install Pandas

pip install --upgrade pandas
```

The next step is to set up your configuration. You will see the file _ConfigTemplate.py_. Copy this file to _Config.py_ and edit your settings. You will need your username and password for logging into Snowflake, the account ID, and the Warehouse and Database names. To find your account ID, simply look at your snowflake URL. It will be something like https://12345.snowflakecomputing.com. 12345 is your account number.

To verify your settings, run `python verify.py`. This will print out the version of Snowflake you are running. 

Assuming the verification works, you can simply run the three scripts by typing python followed by the file name.