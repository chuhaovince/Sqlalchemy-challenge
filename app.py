from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database step

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base =  automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask step

app = Flask(__name__)

@app.route("/")
def homepage():
    return (
        f"Welcome to the Climte App API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/20130101<br/>"
        f"/api/v1.0/start_end_date/20130101/20160101<br/>"
    )

@app.route('/api/v1.0/precipitation')
def prcp():
    session = Session(engine)
    prcp_dict = {}
    results = session.query(Measurement.date, Measurement.prcp).all()
    for item in results:
        # update the dict with date as the key and prcp as the value
        prcp_dict[item[0]] = item[1]
    session.close()
    return jsonify(prcp_dict)

@app.route('/api/v1.0/stations')
def  stations():
    session = Session(engine)
    station = []
    results = session.query(Station.station).group_by(Station.station).all()
    for item in results:
        station_dict = {}
        station_dict["station"] = item
        # create the stations as a list of dictionaries
        # or just do 
        # station += item    to get all the unique stations as a list
        station.append(station_dict)
    session.close()
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.)
    session.close()

if __name__ == "__main__":
    app.run(debug=True)