# msimulator
Tool to use with mongoDB to simulate users interacting with your database for a specified amount of time. Type of data input into database can be specified.

This tool was originally created to generate test log data. 

# Installation
Use `pipenv` to install libraries listed in the Pipfile

# Getting Started
```
python3 main.py <time> [--minutes][--host="localhost"] [--port="27017"] [--number=1]
```
Where `time` is the number of seconds to run this script. Having the `--minutes` flag set will convert your time into minutes and `--hours` flag will convert to hours.

By default, the script will connect to `localhost:27017`.

`--number` allows you to specify the number of processes to spawn in parallel.


# Scenarios
Program will generate a random data entry and pick a random scenario listed below:
 * Insert document
 * Delete document
 * Update document
 * Count number of documents
 * Query document
 * Query document based on range