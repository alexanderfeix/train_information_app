from typing import List
from datetime import datetime
from backend.journey_model import Journey, Arrival, Departure, Station, Connection, ConnectionType, Stop, ConnectionInformation
import uuid


def create_connection(name: str, connection_type: str, departure: Station, departure_datetime: datetime,
                      departure_delay: int, departure_platform: str, arrival: Station, arrival_datetime: datetime,
                      arrival_delay: int, arrival_platform: str, duration: int, stops: List[str],
                      canceled_stops: List[str], text_information: str, connection_code: str):
    """
    Builder function for the connection object.
    :param name: name of the connection, e.g. Munich - Hamburg
    :param connection_type: transport type, e.g. ICE
    :param departure: departure station object
    :param departure_datetime: departure datetime
    :param departure_delay: delay of departure in minutes
    :param departure_platform: platform of departure as string, e.g. 8 C-F
    :param arrival: arrival station object
    :param arrival_datetime: arrival datetime
    :param arrival_delay: delay of arrival in minutes
    :param arrival_platform: platform of arrival as string, e.g. 4
    :param duration: duration of the connection in minutes
    :param stops: list of stops, represented as strings
    :param canceled_stops: list of canceled stops, represented as strings
    :param text_information: any text information relevant to the connection
    :param connection_code: name of the transportation vehicle, e.g. ICE 123
    :return: connection object
    """
    identifier = str(uuid.uuid4())
    connection = create_connection_type(connection_type)
    arrival_type = Arrival(arrival, arrival_datetime, arrival_platform, arrival_delay)
    departure_type = Departure(departure, departure_datetime, departure_platform, departure_delay)
    stops_type = [create_stop(identifier, stop, 0) for stop in stops]
    canceled_stops_type = [create_stop(identifier, canceled_stop, 0) for canceled_stop in canceled_stops]
    information_type = create_information(text_information, canceled_stops_type, 0, connection_code)
    return Connection(identifier, name, connection, departure_type, arrival_type, duration,
                      stops_type, information_type)


def create_journey(name: str, duration: int, connections: List[Connection]):
    """
    Builder function for the journey object.
    :param name: name of the journey, e.g. Munich - Fürth
    :param duration: duration of the journey in minutes
    :param connections: list of connection objects
    :return: journey object, most abstract object in the model
    """
    identifier = str(uuid.uuid4())
    departure_type = connections[0].departure
    arrival_type = connections[-1].arrival
    information = ""
    for connection in connections:
        information += f"{connection.information.text} "
    return Journey(identifier, name, departure_type, arrival_type, duration, connections, information)


def create_connection_type(connection_type: str):
    """
    Create a connection type object from a string.
    :param connection_type: string representation of the connection type, e.g. ICE
    :return: connection type enum object
    """
    connection_type = connection_type.upper()
    for connection in ConnectionType:
        if connection.name == connection_type:
            return connection
    for connection in ConnectionType:
        for detailed in connection.value:
            if detailed.name == connection_type:
                return connection.value[detailed.name]
    return ConnectionType.UNKNOWN


def create_stop(connection: str, station: str, delay: int):
    """
    Builder function for the stop object.
    :param connection: uuid from the connection
    :param station: station name as string
    :param delay: current departure delay in minutes
    :return: stop object
    """
    identifier = str(uuid.uuid4())
    station_type = create_station(station, None)
    return Stop(identifier, connection, station_type, delay)


def create_information(text: str, canceled_stops: List[Stop], delay: int, connection_code: str):
    """
    Builder function for the information object.
    :param text: string with information about the connection
    :param canceled_stops: list of canceled stops, transportation vehicle will not stop at these stations
    :param delay: current delay of the connection in minutes
    :param connection_code: name of the transportation vehicle, e.g. ICE 123
    :return: information object
    """
    identifier = str(uuid.uuid4())
    return ConnectionInformation(identifier, text, canceled_stops, delay, connection_code)


def create_station(name: str, identifier: str = None):
    """
    Builder function for the station object.
    :param name: name of the station as string
    :param identifier: uuid of the station. If not provided, a new uuid will be generated
    :return: station object
    """
    station_identifier = identifier if identifier else str(uuid.uuid4())
    #TODO: Add more information about the station
    return Station(station_identifier, name, None, None)
