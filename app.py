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
        f"/api/v1.0/start_end_date/<start>/<end><br/>"
    )

if __name__ == "__main__":
    app.run(debug=True)