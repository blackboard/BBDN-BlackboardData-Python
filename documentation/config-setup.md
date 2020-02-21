# Setting up your Config.py

The next step is to set up your configuration. You will see the file _ConfigTemplate.py_. Copy this file to _Config.py_ and edit your settings. You will need your username and password for logging into Snowflake, the account ID, and the Warehouse and Database names. To find your account ID, simply look at your snowflake URL. It will be something like https://12345.snowflakecomputing.com. 12345 is your account number.

To verify your settings, run `python verify.py`. This will print out the version of Snowflake you are running.

Assuming the verification works, you can simply run the three scripts by typing python followed by the file name.

You can also run the demo to let it run all demo queries and see them in action using the bbdn_utils module:

```
python3 ./Demo.py
```

Please go here to the next step: [Running verify.py](/documentation/running-verify.md)
