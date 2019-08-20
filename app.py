import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#####################################################
# Database Setup
#####################################################

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


#######################################################
# Flask Setup
#######################################################
app = Flask(__name__)


#######################################################
# Flask Routes
#######################################################

@app.route("/")
def welcome():
    return(
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precip():

    

    most_recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago=dt.date(2017, 8, 23)-dt.timedelta(days=365)
    
    prec_scores=session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date).all()
    
    session.close()
    
    prcp_dict=dict(prec_scores)

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
   
    session = Session(engine)

    station_count = session.query(Measurement.station).distinct()
    return jsonify([station[0] for station in station_count])

    session.close()

@app.route("/api/v1.0/tobs")
def tobs():

    #recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #yearago=dt.date(2017, 8, 8)-dt.timedelta(days=365)

    session = Session(engine)
    tobs_scores=session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date >= '2016-08-08').\
        order_by(Measurement.date).all()

    session.close()

    tobs_dict=dict(tobs_scores)
    return jsonify(tobs_dict)

if __name__ == '__main__':
    app.run(debug=True)
