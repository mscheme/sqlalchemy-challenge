import numpy as np
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    #return list of api routes
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    # Return the JSON representation of your dictionary.
    precip={}
    # find the latest date in the data set
    max_date = session.query(func.max(Measurement.date)).first()[0]

    # subtract one year from the max date
    prev_year_date = dt.datetime.strptime(max_date, '%Y-%m-%d') - relativedelta(years=1)

    query_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year_date).all()

    for row in query_results:
        date = (row[0])
        prcp = (row[1])

        precip[date] = prcp
    
    return jsonify(precip)

if __name__ == '__main__':
    app.run()