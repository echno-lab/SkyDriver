import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Flight:
    first_departure_airport: str
    first_airline: str
    first_departure_date: datetime
    first_arrival_airport: str
    first_arrival_date: datetime
    first_arrival_duration: str
    second_departure_airport: str = None
    second_departure_date: datetime = None
    second_airline_logo: str = None
    second_airline: str = None
    second_arrival_airport: str = None
    second_arrival_date: datetime = None
    second_arrival_duration: str = None
    stop_time: datetime = None

    def dict(self):
        data = {}
        for field_name, field_obj in self.__dataclass_fields__.items():
            value = getattr(self, field_name)
            if value is not None:  # Skip fields with None values
                data[field_name] = value
        return data


@dataclass
class InboundFlight(Flight):
    pass


@dataclass
class OutboundFlight(Flight):
    price: str = None
    id: int = None


class FlightProcessor:
    def __init__(self, flight_data: dict):
        self.flight_data = flight_data
        self.inbound_flight = InboundFlight
        self.outbound_flight = OutboundFlight
        self.flights = [self.outbound_flight, self.inbound_flight]

    def get_flights(self) -> list[InboundFlight, OutboundFlight]:
        self._get_price_and_id()
        flights = self._construct_flights()
        return flights

    def _get_price_and_id(self):
        self.outbound_flight.price = self.flight_data["price"]["total"]
        self.outbound_flight.id = self.flight_data["id"]

    def _construct_flights(self) -> list[InboundFlight, OutboundFlight]:
        i = 0
        flights = []
        for _ in self.flight_data["itineraries"]:
            if i == 0:
                flight = self.outbound_flight
            else:
                flight = self.inbound_flight

            flight.first_departure_airport = self.flight_data["itineraries"][i]["segments"][0][
                "departure"
            ]["iataCode"]
            flight.first_airline = self.flight_data["itineraries"][i]["segments"][0]["carrierCode"]
            flight.first_departure_date = get_hour(
                self.flight_data["itineraries"][i]["segments"][0]["departure"]["at"]
            )
            flight.first_arrival_airport = self.flight_data["itineraries"][i]["segments"][0][
                "arrival"
            ]["iataCode"]
            flight.first_arrival_date = get_hour(
                self.flight_data["itineraries"][i]["segments"][0]["arrival"]["at"]
            )
            flight.first_arrival_duration = self.flight_data["itineraries"][i]["segments"][0][
                "duration"
            ]

            if len(self.flight_data["itineraries"][i]["segments"]) > 1:
                flight.second_departure_airport = self.flight_data["itineraries"][i]["segments"][1][
                    "departure"
                ]["iataCode"]
                flight.second_airline = self.flight_data["itineraries"][i]["segments"][1][
                    "carrierCode"
                ]
                flight.second_departure_date = get_hour(
                    self.flight_data["itineraries"][i]["segments"][1]["departure"]["at"]
                )
                flight.second_arrival_airport = self.flight_data["itineraries"][i]["segments"][1][
                    "arrival"
                ]["iataCode"]
                flight.second_arrival_date = get_hour(
                    self.flight_data["itineraries"][i]["segments"][1]["arrival"]["at"]
                )
                flight.second_arrival_duration = self.flight_data["itineraries"][i]["segments"][1][
                    "duration"
                ]
            #  stop_time = get_stoptime(
            #      self.flight_data["itineraries"][i]["duration"],
            #      flight.first_.arrival_duration,
            #      flight.second_arrival_duration,
            #  )
            flights.append(flight)
            i += 1
        return flights


def get_hour(date_time: str):
    return datetime.strptime(date_time[0:19], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")


def get_stoptime(total_duration: str, first_flight_duration: str, second_flight_duration: str):
    total_duration = re.findall(r"\d+", total_duration)
    total_duration = int(total_duration[0]) * 60 + int(total_duration[1])
    first_flight_duration = re.findall(r"\d+", first_flight_duration)
    first_flight_duration = int(first_flight_duration[0]) * 60 + int(first_flight_duration[1])
    second_flight_duration = re.findall(r"\d+", second_flight_duration)
    second_flight_duration = int(second_flight_duration[0]) * 60 + int(second_flight_duration[1])
    return total_duration - (first_flight_duration + second_flight_duration)
