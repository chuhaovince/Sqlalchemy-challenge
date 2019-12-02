from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
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
        f"/api/v1.0/start_date/2013-01-01<br/>"
        f"/api/v1.0/start_end_date/2013-01-01/2016-01-01<br/>"
    )

@app.route('/api/v1.0/precipitation')
def prcp():
    session = Session(engine)
    prcp = []
    results = session.query(Measurement.date, Measurement.prcp).all()
    for item in results:
        prcp_dict = {}
        # update the dict with date as the key and prcp as the value
        prcp_dict['date'] = item[0]
        prcp_dict['prcp'] = item[1]
        prcp.append(prcp_dict)
    session.close()
    return jsonify(prcp)

@app.route('/api/v1.0/stations')
def  stations():
    session = Session(engine)
    station = []
    results = session.query(Station.station).group_by(Station.station).all()
    for item in results:
        station_dict = {}
        station_dict["station"] = item[0]
        # create the stations as a list of dictionaries
        # or just do 
        # station += item    to get all the unique stations as a list
        station.append(station_dict)
    session.close()
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_entry = session.query(Measurement.date, func.max(Measurement.id)).all()
    last_date = dt.datetime.strptime(last_entry[0][0], "%Y-%m-%d")
    date_1_year_ago = (last_date - dt.timedelta(days = 365)).strftime("%Y-%m-%d")
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= date_1_year_ago).all()
    tobs = []
    for row in results:
        tob_dict = {}
        tob_dict["date"] = row[0]
        tob_dict["temp"] = row[1]
        tobs.append(tob_dict)
    session.close()
    return jsonify(tobs)


@app.route("/api/v1.0/start_date/<start_date>")
def dates_no_end(start_date):
    session = Session(engine)
    
    # if end date is not given by user
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    return jsonify({"Max Temp" : results[0][2], "Min Temp": results[0][0], "Avg Temp" : results[0][1]})


@app.route("/api/v1.0/start_end_date/<start_date>/<end_date>")
def dates(start_date,end_date):
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    session.close()
    return jsonify({"Max Temp" : results[0][2], "Min Temp": results[0][0], "Avg Temp" : results[0][1]})



if __name__ == "__main__":
    app.run(debug=True)