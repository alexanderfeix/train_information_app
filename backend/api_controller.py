from pyhafas import HafasClient
from pyhafas.profile import DBProfile
from backend.journey_controller import create_station, create_connection, create_journey
from datetime import datetime

client = HafasClient(DBProfile())


def load_journey(departure_station_name: str, departure_station_datetime: datetime, arrival_station_name: str):
    """
    Load a journey from the HAFAS API.
    :param departure_station_name: station name as string
    :param departure_station_datetime: station datetime
    :param arrival_station_name: station name as string
    :return: journey object as defined in journey_model
    """
    departure_station = _load_stations(departure_station_name)[0]
    arrival_station = _load_stations(arrival_station_name)[0]
    journeys = client.journeys(departure_station.identifier, arrival_station.identifier,
                               departure_station_datetime, max_journeys=5)
    for journey in journeys:
        journey_duration = journey.duration.seconds // 60
        journey_connections = []
        for connection in journey.legs:
            departure = _load_stations(connection.origin.name)[0]
            departure_delay = connection.departureDelay.seconds // 60 if connection.departureDelay else 0
            arrival = _load_stations(connection.destination.name)[0]
            arrival_delay = connection.arrivalDelay.seconds // 60 if connection.arrivalDelay else 0
            duration = (connection.arrival - connection.departure).seconds // 60
            stops, remarks, canceled_stops, canceled_stops_remarks = [], [], [], []
            if connection.stopovers:
                for stop in connection.stopovers:
                    stops.append(stop.stop.name)
                    if stop.cancelled:
                        canceled_stops.append(stop.stop.name)
                        canceled_stops_remarks.append([remark.text for remark in stop.remarks])
            information_text = ""
            for remark in connection.remarks:
                information_text += f"{remark.text};"
            if connection.name:
                connection_mode = connection.name.split(" ")[0]
            else:
                connection_mode = "WALKING"

            journey_connection = create_connection(connection.name, connection_mode, departure, connection.departure,
                                                   departure_delay, connection.departurePlatform, arrival,
                                                   connection.arrival, arrival_delay, connection.arrivalPlatform,
                                                   duration, stops, canceled_stops, information_text,
                                                   connection.name)
            journey_connections.append(journey_connection)
        return create_journey(f"{departure_station_name} - {arrival_station_name}",
                              journey_duration, journey_connections)


def _load_stations(name: str):
    """
    Load stations from the Hafas API.
    :param name: station name as string
    :return: station object as defines in journey_model
    """
    stations = []
    for station in client.locations(name):
        stations.append(create_station(station.name, station.id))
    return stations
