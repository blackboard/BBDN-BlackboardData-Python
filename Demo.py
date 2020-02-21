from bbdn_utils import run_query
from app_config import app_config
run_query('current-version')
run_query('current-version', app_config['currentVersion'])
run_query('time-spent-in-learn', app_config['timeSpentInLearn'])
run_query('time-spent-in-collab', app_config['timeSpentInCollab'])
run_query('activity-equals-success', app_config['activityEqualsSuccess'])
