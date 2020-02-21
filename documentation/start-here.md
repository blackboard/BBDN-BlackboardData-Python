# Start Here Guide

## Setting Up Your Environment

This project was built with Python 3.7. Other versions may work, but have not been tested. The project itself requires four Python Libraries:

-   Snowflake Python Connector
-   Snowflake Python Connecter Pandas Updates
-   Pandas
-   Matplotlib
-   pyarrow (peer dependency and may need to be installed)

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

Please view the next step: Setting up you Config.py
