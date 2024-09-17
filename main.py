from backend.api_controller import load_journey
from backend.journey_controller import Journey
from datetime import datetime, timedelta
from flask import Flask, request, render_template

"""
Main application file for the Flask web server.
"""

app = Flask(__name__)


def get_next_train_for_trip(departure_station: str, departure_station_datetime: datetime, arrival_station: str):
    journey: Journey = load_journey(departure_station, departure_station_datetime, arrival_station)
    next_departure = (journey.departure.datetime.replace(tzinfo=None) + timedelta(0, journey.departure.delay * 60)) - departure_station_datetime.replace(tzinfo=None)
    return (f"The next train from {departure_station} to {arrival_station} departs in {next_departure.seconds // 60 // 60}h {next_departure.seconds // 60 % 60}min from "
            f"platform {journey.departure.platform}."), journey


@app.route("/search", methods=["GET", "POST"])
def start_flask():
    train_info = ""
    train_data = None
    departure_station = ""
    arrival_station = ""
    departure_date = datetime.now().strftime("%Y-%m-%d")
    departure_time = datetime.now().strftime("%H:%M")
    if request.method == "POST":
        try:
            departure_station = request.form["departure_station"]
            departure_date = request.form["departure_date"] if request.form["departure_date"] else departure_date
            departure_time = request.form["departure_time"] if request.form["departure_time"] else departure_time
            date = datetime.strptime(f"{departure_date}T{departure_time}", "%Y-%m-%dT%H:%M")
            arrival_station = request.form["arrival_station"]
            if departure_station and departure_date and departure_time and arrival_station:
                train_info, train_data = get_next_train_for_trip(departure_station, date, arrival_station)
            else:
                train_info = "Please fill out all data fields."
        except Exception as e:
            train_info = f"Error loading data: {e}"
    return render_template('index.html', train_string=train_info, train_data=train_data,
                           departure=departure_station, arrival=arrival_station, date=departure_date,
                           time=departure_time)


if __name__ == "__main__":
    app.run(debug=True)
