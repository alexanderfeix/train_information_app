from datetime import datetime
from typing import List
from enum import Enum, auto


class TrainType(Enum):
    ICE = auto()
    IC = auto()
    RE = auto()
    RB = auto()
    NJ = auto()
    S = auto()
    U = auto()


class ConnectionType(Enum):
    TRAIN = TrainType
    BUS = auto()
    TRAM = auto()
    SUBWAY = auto()
    FERRY = auto()
    WALKING = auto()
    BIKE = auto()
    CAR = auto()
    TAXI = auto()
    SHUTTLE = auto()
    PARKING = auto()
    CHANGE = auto()
    WAIT = auto()
    UNKNOWN = auto()


class Station:
    def __init__(self, identifier: str, name: str, city: str, country: str):
        self.identifier = identifier
        self.name = name
        self.city = city
        self.country = country


class Departure:
    def __init__(self, station: Station, date_time: datetime, platform: str = None, delay: int = 0):
        self.station = station
        self.datetime = date_time
        self.platform = platform
        self.delay = delay


class Arrival:
    def __init__(self, station: Station, date_time: datetime, platform: str = None, delay: int = 0):
        self.station = station
        self.datetime = date_time
        self.platform = platform
        self.delay = delay


class Stop:
    def __init__(self, identifier: str, connection_identifier: str, station: Station, delay: int):
        self.identifier = identifier
        self.connection = connection_identifier
        self.station = station
        self.delay = delay


class ConnectionInformation:
    def __init__(self, identifier: str, text: str, canceled_stops: List[Stop], current_delay: int,
                 connection_code: str = ""):
        self.identifier = identifier
        self.text = text
        self.canceled_stops = canceled_stops
        self.current_delay = current_delay
        self.connection_code = connection_code


class Connection:
    def __init__(self, identifier: str, name: str, connection_type: ConnectionType, departure: Departure,
                 arrival: Arrival, duration: int, stops: List[Stop], information: ConnectionInformation):
        self.identifier = identifier
        self.name = name
        self.connection_type = connection_type
        self.departure = departure
        self.arrival = arrival
        self.duration = duration
        self.stops = stops
        self.information = information


class Journey:
    def __init__(self, identifier: str, name: str, departure: Departure, arrival: Arrival, duration: int,
                 connections: List[Connection], journey_information: str):
        self.identifier = identifier
        self.name = name
        self.departure = departure
        self.arrival = arrival
        self.duration = duration
        self.connections = connections
        self.information = journey_information
