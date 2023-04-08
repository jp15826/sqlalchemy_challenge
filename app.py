# Import the dependencies.

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd
import datetime as dt

# create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base=automap_base()
base.prepare(autoload_with=engine)
base.classes.keys()
# Save references to each table
Measurement=base.classes.measurement
Station=base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

# Flask Setup
app=Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    return(
        f"select from one of the avaliable routes"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/start/end"
        
    )

#api/precipitation
@app.route("/api/v1.0/precipitation")
def prec():
    oneYear = dt.date (2017,8,23) - dt.timedelta (days=365)
    twelveMonths= session.query(Measurement.date, Measurement.prcp).filter (Measurement.date >= oneYear).all()

    session.close()

    precip={date: precipitation for date, precipitation in twelveMonths}

    return jsonify (precip)

#api/stations

@app.route("/api/v1.0/stations")
def stat():
    twelveMonths= session.query(Station.station).all()

    stations=list(np.ravel(twelveMonths))

    return jsonify(stations)

#api/stations
@app.route("/api/v1.0/tobs")
def tobs():
    oneYear = dt.date (2017,8,23) - dt.timedelta (days=365)
    tob=session.query(Measurement.tobs).filter (Measurement.station=='USC00519281').filter(Measurement.date >= oneYear).all()

    session.close()

    list1=list(np.ravel(tob))

    return jsonify (list1)

#api/start/end

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start=None, end=None):

    x=[func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]

    if not end:

        start:dt.datetime.strptime(start)

        data=session.query.filter(Measurement.date >=start).all()

        session.close()

        list2=list(np.ravel(x))

        return (list2)


if __name__ == "__main__":
    app.run(debug=True)