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
    # Return the precipitation data for the last year
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    # Return the JSON representation of your dictionary.
    precip={}

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # find the latest date in the data set
    max_date = session.query(func.max(Measurement.date)).first()[0]

    # subtract one year from the max date
    prev_year_date = dt.datetime.strptime(max_date, '%Y-%m-%d') - relativedelta(years=1)

    query_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year_date).all()

    # close session
    session.close()

    for row in query_results:
        date = (row[0])
        prcp = (row[1])

        precip[date] = prcp
    
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Return a JSON list of stations from the dataset
    station_results = session.query(Station.station).all()

    #close session
    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_results))

    return jsonify(station_list = station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    max_date = session.query(func.max(Measurement.date)).first()[0]

    # subtract one year from the max date
    prev_year_date = dt.datetime.strptime(max_date, '%Y-%m-%d') - relativedelta(years=1)

    # identify the most active station
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).\
    all()

    most_active_station = active_stations[0][0]

    # query the tobs for the station over the last yera of data
    active_station_obs = session.query(Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
            filter(Measurement.date >= prev_year_date).all()

    # close session
    session.close

     # Convert list of tuples into normal list
    tobs_list = list(np.ravel(active_station_obs))

    return jsonify(Temperature_Observations = tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def minAvgMax(start=None, end=None):
    #Return a JSON list of:
    # the minimum temperature, the average temperature, and the max temperature 
    # for a given start or start-end range.

    # define select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #When given the start only, calculate TMIN, TAVG, and TMAX 
    # for all dates greater than and equal to the start date.
    if not end:
        start_results = session.query(*sel).filter(Measurement.date >= start).all()

        # Convert list of tuples into normal list
        start_list = list(np.ravel(start_results))
        
        return jsonify(Temperatures = start_list)

    #When given the start and the end date, calculate the TMIN, TAVG, and TMAX 
    # for dates between the start and end date inclusive.
    st_end_results = session.query(*sel).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # close session
    session.close()

    # Convert list of tuples into normal list
    st_end_list = list(np.ravel(st_end_results))
        
    return jsonify(Temperatures = st_end_list)


if __name__ == '__main__':
    app.run()