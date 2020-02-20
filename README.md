# Blackboard Data Python Demos

This project contains three sample scripts to run queries against Blackboard Data, pull them into Pandas Dataframes, and export the data to CSV files. In these samples, we have three queries:

-   **Time Spent In Learn**

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

-   **Time Spent In Collab**

```
select
  count(distinct room_id) as room_count,
  count(id) as session_count,
  session_count / room_count as avg_sessions_per_room,
  sum(attended_duration/60) as session_minutes_sum
from cdm_clb.session
where attended_duration > 0
```

-   **Activity Equals Success**

```
select
  grade_band,
  round(avg(ns_clean),2) as avg_grade,
  round(avg(total_duration_sum)/60,0) as avg_course_minutes,
  round(avg(total_interaction_cnt),0) as avg_course_interactions,
  round(avg(course_access_cnt),0) as avg_course_accesses,
  round(avg(clb_duration_sum)/60,0) as avg_collab_minutes,
  round(avg(clb_access_cnt),2) as avg_collab_accesses
from
( -- SUMMARIZE COURSE ACTIVITY
    select
        person_course_id,
        course_id,
        person_id,
        sum(duration_sum) as total_duration_sum,
        sum(interaction_cnt) as total_interaction_cnt,
        count(id) as course_access_cnt
    from cdm_lms.course_activity
    group by
        person_course_id,
        course_id,
        person_id
) lms
inner join
( -- SUMMARIZE COLLABORATE ACTIVITY
    select
        mcr.lms_course_id,
        mp.lms_person_id,
        sum(ca.duration) as clb_duration_sum,
        count(ca.id) as clb_access_cnt
    from cdm_clb.attendance ca
    inner join cdm_clb.session cs
        on ca.session_id = cs.id
    inner join cdm_map.course_room mcr
        on cs.room_id = mcr.clb_room_id
    inner join cdm_map.person mp
        on mp.clb_person_id = ca.person_id
    group by
        mcr.lms_course_id,
        mp.lms_person_id
) clb
    on clb.lms_course_id = lms.course_id
    and clb.lms_person_id = lms.person_id
inner join
( -- GET TOTAL COURSE GRADE
  select
      lg.person_course_id as lpc_id,
      lg.normalized_score,
      case
          when lg.normalized_score > 1 then 1
          when lg.normalized_score < 0 then 0
          else lg.normalized_score
      end as ns_clean,
      ntile(4) over (order by ns_clean) as grade_band
  from cdm_lms.grade lg
  inner join cdm_lms.gradebook lgb
      on lg.gradebook_id = lgb.id
      and lgb.final_grade_ind = 1
      and deleted_ind = 0
  where normalized_score is not null
) grd
    on grd.lpc_id = lms.person_course_id
group by grade_band
order by grade_band
```

## Setting Up Your Environment

This project was built with Python 3.7. Other versions may work, but have not been tested. The project itself requires four Python Libraries:

-   Snowflake Python Connector
-   Snowflake Python Connecter Pandas Updates
-   Pandas
-   Matplotlib

To install the libraries, use `pip`:

```
# Install Snowflake Python Connector

pip install --upgrade snowflake-connector-python

# Install Snowflake Python Connector Pandas Updates
# Double quotes required on MacOS, not required on windows

pip install "snowflake-connector-python[pandas]"

# Install Pandas

pip install --upgrade pandas

# Install matplotlib

pip install --upgrade matplotlib
```

Or you can use the requirements.txt install method. This can be done either in your venv (virutal environment) or on your system python3 version.

```
python3 -m pip install --user -r ./requirements.txt
```

The next step is to set up your configuration. You will see the file _ConfigTemplate.py_. Copy this file to _Config.py_ and edit your settings. You will need your username and password for logging into Snowflake, the account ID, and the Warehouse and Database names. To find your account ID, simply look at your snowflake URL. It will be something like https://12345.snowflakecomputing.com. 12345 is your account number.

To verify your settings, run `python verify.py`. This will print out the version of Snowflake you are running.

Assuming the verification works, you can simply run the three scripts by typing python followed by the file name.
