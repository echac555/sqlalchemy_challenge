# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:////Users/chac/Desktop/Class/Module_10_Assignment/sqlalchemy_challenge/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement=Base.classes.measurement
station=Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################

app=Flask(__name__)


#################################################
# Flask Routes
#################################################

#1./
#Start at the homepage.
#List all the available routes.

@app.route("/")
def welcome():
    """List available API routes"""
    return(
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'
    )

#2. /api/v1.0/precipitation
#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitaion():
    last_year=dt.date(2017, 8, 23)-dt.timedelta(days=365)
    last_year
    last_year_data=session.query(measurement.date, measurement.prcp).\
    filter(measurement.date>=last_year).\
    order_by(measurement.date).all()
    precipitaion={date: prcp for date, prcp in last_year_data}
    return jsonify(precipitaion)

#3. /api/v1.0/stations
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(measurement.station).distinct().all()
    station_list
    stations = list(np.ravel(station_list))
    return jsonify(stations)

#4. /api/v1.0/tobs
#Query the dates and temperature observations of the most-active station for the previous year of data.
#Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def temperature():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year
    last_year_data = session.query(measurement.station , measurement.tobs).\
        filter(measurement.station =="USC00519281").\
        filter(measurement.date >=last_year).\
        order_by(measurement.date).all()
    temperature = list(np.ravel(last_year_data))
    return jsonify(temperature)

#5. /api/v1.0/<start> and /api/v1.0/<start>/<end>
#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def averages(start=None, end=None):

    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year
    temp = [measurement.station,
           func.min(measurement.tobs),
           func.max(measurement.tobs),
           func.avg(measurement.tobs)]
    if not end:
        temp_averages = session.query(*temp).\
            filter(measurement.date >= last_year).\
            filter(measurement.date <= last_year).all()
        data = list(np.ravel(temp_averages))
        return jsonify(data=data)

if __name__ == "__main__":
    app.run(debug=True)