# sqlalchemy-challenge

See HW_instructions.md for details on this assignment.

The jupyter notebook file demonstrates using SQLAlchemy to connect to a sqlite database.
Once connected, the database and tables are relfected into the notebook for use.
Examples of queries are run using SQLAlchemy ORM queries.
Results are stored into a Pandas database and displayed on plots.

Additionally a Flask App was created.
Using SQLAlchemy once again, the sqlite database is connected to the flask file.
Some of the same queries are used in the app routes.
The results of the queries of the different routes are displayed in a JSON format.
The routes are displayed on the home route.
