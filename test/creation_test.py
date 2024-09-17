import unittest
from datetime import datetime
from backend.journey_controller import create_connection, create_journey, create_station


class CreationTests(unittest.TestCase):
    def test_journey_creation(self):
        first_departure = create_station("München Hbf", None)
        first_arrival = create_station("Erfurt Hbf", None)
        first_departure_datetime = datetime(2024, 9, 9, 20, 40)
        first_departure_delay = 5  # 5 minutes delay
        first_departure_platform = "5 C-F"
        first_arrival_datetime = datetime(2024, 9, 10, 0, 40)
        first_arrival_delay = 1
        first_arrival_platform = "8"
        first_duration = 60 * 5
        first_stops = ["Augsburg Hbf", "Treuchtlingen", "Nürnberg Hbf", "Erfurt Hbf", "Hannover Hbf"]
        first_canceled_stops = ["Augsburg Hbf"]
        first_text_information = "Der Zug fährt heute nicht über Augsburg."
        first_connection_type = "ICE"
        first_connection_code = "ICE 466"
        first_connection = create_connection("München - Erfurt", first_connection_type, first_departure,
                                             first_departure_datetime, first_departure_delay, first_departure_platform,
                                             first_arrival, first_arrival_datetime, first_arrival_delay,
                                             first_arrival_platform, first_duration, first_stops, first_canceled_stops,
                                             first_text_information, first_connection_code)

        second_departure = create_station("Erfurt Hbf", None)
        second_arrival = create_station("Hamburg Hbf", None)
        second_departure_datetime = datetime(2024, 9, 10, 1, 20)
        second_arrival_datetime = datetime(2024, 9, 10, 3, 0)
        second_duration = 100
        second_stops = ["Erfurt Hbf", "Hannover Hbf"]
        second_canceled_stops = []
        second_text_information = "Der Zug fährt wie geplant."
        second_connection_type = "ICE"
        second_connection = create_connection("Erfurt - Hamburg", second_connection_type, second_departure,
                                              second_departure_datetime, 0, "9", second_arrival,
                                              second_arrival_datetime, 0, "5", second_duration,
                                              second_stops, second_canceled_stops, second_text_information, "ICE 599")

        third_departure = create_station("Hamburg Hbf", None)
        third_arrival = create_station("Kiel", None)
        third_departure_datetime = datetime(2024, 9, 10, 3, 20)
        third_arrival_datetime = datetime(2024, 9, 10, 4, 42)
        third_duration = 82
        third_stops = []
        third_canceled_stops = []
        third_text_information = ""
        third_connection_type = "RE"
        third_connection = create_connection("Hamburg Hbf - Kiel", third_connection_type, third_departure,
                                             third_departure_datetime, 2, "9F",  third_arrival,
                                             third_arrival_datetime, 4, "3", third_duration, third_stops,
                                             third_canceled_stops, third_text_information, "RE 9")

        connections = [first_connection, second_connection, third_connection]
        journey = create_journey("München Hbf - Kiel", 8*60+2, connections)
        self.assertEqual(8*60+2, journey.duration)
        self.assertEqual("München Hbf - Kiel", journey.name)
        self.assertEqual("München Hbf", journey.connections[0].departure.station.name)

    def test_connection_creation(self):
        departure = create_station("München Hbf", None)
        arrival = create_station("Nürnberg Hbf", None)
        departure_datetime = datetime(2024, 9, 9, 20, 40)
        departure_delay = 4
        departure_platform = "1"
        arrival_datetime = datetime(2024, 9, 9, 22, 46)
        arrival_delay = 2
        arrival_platform = "4 C-F Ost"
        duration = 126
        stops = ["Donauwörth", "Treuchtlingen", "Schwabach"]
        canceled_stops = ["Donauwörth"]
        text_information = "Der Zug fährt heute nicht über Donauwörth."
        connection_type = "RE"
        connection_code = "RE 16"
        connection = create_connection("München - Nürnberg", connection_type, departure, departure_datetime,
                                       departure_delay, departure_platform, arrival, arrival_datetime, arrival_delay,
                                       arrival_platform, duration, stops, canceled_stops, text_information,
                                       connection_code)
        self.assertIsNotNone(connection)
        self.assertEqual(connection.name, "München - Nürnberg")
        self.assertEqual(connection.connection_type.name, connection_type)
        self.assertEqual(connection.information.text, text_information)
        self.assertEqual(connection.departure.station.name, departure.name)
        self.assertEqual(connection.arrival.station.name, arrival.name)
        self.assertEqual(connection.departure.platform, departure_platform)
        self.assertEqual(connection.arrival.platform, arrival_platform)
        self.assertEqual(connection.information.connection_code, connection_code)
        self.assertEqual(connection.departure.delay, departure_delay)
        self.assertEqual(connection.arrival.delay, arrival_delay)
        print(f"ID: {connection.identifier}")


if __name__ == '__main__':
    unittest.main()
