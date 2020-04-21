import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# DataBase Setup
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
#Measurement = Base.classes.measurement
#Station = Base.classes.station


#Create Flask
app = Flask(__name__)

@app.route("/")
def home():
    # Print message on server
    print("Server received request for 'Home' page...")
    # Return result to client (print message on client)
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#@app.route("/api/v1.0/precipitation")



#@app.route("/api/v1.0/stations")



#@app.route("/api/v1.0/tobs")



#@app.route("/api/v1.0/<start>")



#@app.route("/api/v1.0/<start>/<end>")

if __name__ == "__main__":
    app.run(debug=True)