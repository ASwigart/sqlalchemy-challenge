from datetime import date
import numpy as np
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func

from flask import Flask, jsonify
######################################
# Database
######################################
engine = create_engine("sqlite:///hawaii.sqlite")
# New Model
Base = automap_base()
# reflect tables
Base.prepare(autoload_with=engine, reflect=True)
Base.classes.keys
# reference to table
Measurement = Base.classes.measurement
Stations = Base.classes.station

################################
# Flask
###############################
app=Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/preciptation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/preciptation")
def preciptation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp). all()
    session.close()
# ?One route
    results = list(np.ravel(results))
    return jsonify(results)
# ?another route
    # preciptation = []
    # for date and preciptation in results:
    #     preciptation_dict = {}
    #     preciptation_dict["date"]=date
    #     preciptation_dict["prcp"]=preciptation 
    #     return jsonify(preciptation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Stations.station).all()
    session.close()

    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session= Session(engine)
    tobsresults =session.query(func.count(Measurement.station),Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    session.close()
        
    tempobs=list(np.ravel(tobsresults))
        
    return jsonify(tempobs=tempobs)

@app.route("/api/v1.0/<start_date>")
def calc_starttemps(start_date):
   
    session= Session(engine)
    queryresult =session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    session.close()
    dateresult=list(np.ravel(queryresult))
    
    return jsonify(dateresult=dateresult)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
    #  """TMIN, TAVG, and TMAX for a list of dates.
    
    #  Args:
    #      start_date (string): A date string in the format %Y-%m-%d
    #      end_date (string): A date string in the format %Y-%m-%d
        
    #  Returns:
    #      TMIN, TAVE, and TMAX
    #  """
    session= Session(engine)
    queryresult =session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
    dateresult=list(np.ravel(queryresult))
    
    return jsonify(dateresult=dateresult)
                   
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
