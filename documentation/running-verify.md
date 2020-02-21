# Running verify.py

## What this scipt does.

This script uses the Snowflake connector to connect to your instance of Bb Data. It runs a query:

```
SELECT current_version()
```

This query returns the current version of your Bb Data Snowflake instance. The return data is printed out to the terminal.

## Why having this script could be useful?

You maybe in the need to know what version of Snowflake is running in order to make sure that any third party integrations have been prepped to the changes that could be made from a previous version of Snowflake. Or, you maybe looking for documentation and not sure which version you are running these scripts against.

## How do you run this script?

You can run this script by accessing you terminal of choice (command prompt or PowerShell for Windows users. There is also another option for Windows users call Cmder as well as using Git's integrated bash features.)

Once in your terminal enter the following:

```
python3 ./verify.py
```

Note that here we have python3, this can different for computer setup so please adjust accordingly. We will just use python3 for sake of making it simple.

Once you run that command you should be returned with the current version of Snowflake.

Please go here to see the next step: Running TimeSpentInLearn.py
