import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# DataBase Setup
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Variables for API
session = Session(engine)

last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
start_date = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(366)

station_results = session.query(Measurement.station, func.count(Measurement.station)).\
                group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
most_active_id = station_results[0][0]

#Create Flask
app = Flask(__name__)

#Create Home Page
@app.route("/")
def home():
    
    return (
        f"Welcome to my Hawaii weather API!!!<br/>"
        f"<br/>"
        f"Insert the start-date or start-date/end-date desired in 'YYYY-MM-DD'<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<start><br/>"
        f"/api/v1.0/YYYY-MM-DD<start>/YYYY-MM-DD<end><br/>"
    )

#Create 'precipitation' Route: last 12 months of precipitation data (date and prcp)
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()
    session.close()

    date_prcp = []

    for date, prcp in results:
        date_dict = {}
        date_dict[date] = prcp
        date_prcp.append(date_dict)
        
    return jsonify(date_prcp)

#Create 'stations' Route: list of stations in data set ordered by the most active to the least active 
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_results = session.query(Measurement.station).group_by(Measurement.station).\
                order_by(func.count(Measurement.station).desc()).all()
    session.close()

    return jsonify(station_results)

#Create 'tobs' Route: dates and temperature observations for last 12 months
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    temp_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_id).\
                filter(Measurement.date >= start_date).all()
    session.close()

    return jsonify(temp_results)

#Create a Dynamic 'start-date' Route: min, average, and max temperatures for all dates after start date
@app.route("/api/v1.0/<start>")
def begin(start):
    session = Session(engine)
    begin_date = dt.datetime.strptime(start, "%Y-%m-%d")
    
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= begin_date).all()
    session.close()

    return jsonify(temp_stats)

#Create a Dynamic 'start-date and end-date' Route: min, average, and max temperatures for all dates in between start and end dates
@app.route("/api/v1.0/<start>/<end>")
def finish(start, end):
    session = Session(engine)
    begin_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    
    temp_stats_range = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date.between(begin_date, end_date)).all()
    session.close()

    return jsonify(temp_stats_range)

#run the app
if __name__ == "__main__":
    app.run(debug=True)