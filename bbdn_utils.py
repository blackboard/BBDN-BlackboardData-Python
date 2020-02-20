import os
import snowflake.connector
import pandas as pd
import Config as cfg
from pathlib import Path
from app_config import app_config

APP_ROOT = os.getcwd()
# pd.set_option('display.max_rows', 10)


def load_sql_file(filename):
    return Path(APP_ROOT) / 'queries' / f"{filename}.sql"


def get_connector():
    return snowflake.connector.connect(
        user=cfg.sfconcfg['user'],
        password=cfg.sfconcfg['password'],
        account=cfg.sfconcfg['account'],
        warehouse=cfg.sfconcfg['warehouse'],
        database=cfg.sfconcfg['database'],
        insecure_mode=cfg.sfconcfg['insecure_mode'],
    )


def run_query(query_name, config=None):
    ctx = get_connector()
    cur = ctx.cursor()
    sql = load_sql_file(query_name).read_text()

    if config and config['params']:
        for key, value in config['params'].items():
            sql = sql.replace('{' + key + '}', value)
    print(sql)

    try:
        data = pd.read_sql(sql, ctx)
        # TODO: Fix this for later, use read_sql() for now
        # fetch_pandas_all() causing segfault on linux....???
        # 1]    32279 segmentation fault (core dumped)  python3 ./bbdn_utils.py
        # print(data)
        # cur.execute(sql)
        # df = cur.fetch_pandas_all()
        # print(df.head())
        if config and config['config']:
            data.to_csv(config['config']['outfile'],
                        index=config['config']['index'])
        else:
            print(data)
    finally:
        cur.close()

    ctx.close()


if __name__ == "__main__":
    # run_query('current-version')
    # run_query('current-version', app_config['currentVersion'])
    # run_query('time-spent-in-learn', app_config['timeSpentInLearn'])
    run_query('time-spent-in-collab', app_config['timeSpentInCollab'])
