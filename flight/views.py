import os

from amadeus import Client, ResponseError
from django.shortcuts import get_object_or_404, render
from drf_yasg.utils import swagger_auto_schema

from flight.flight_offer import FlightProcessor
from skydriver.config import AMADEUS_API_KEY, AMADEUS_API_SECRET

from .forms import FlightSearchForm
from .models import Airport

amadeus = Client(
    client_id=AMADEUS_API_KEY,
    client_secret=AMADEUS_API_SECRET,
)


def index(request):
    form = FlightSearchForm()
    airports = Airport.objects.all()
    return render(request, "index.html", {"form": form, "airports": airports})


def search(request):
    if request.method == "GET":
        form = FlightSearchForm(request.GET)
        if form.is_valid():
            kwargs = {
                "originLocationCode": get_iata_code(form.cleaned_data["origin"]),
                "destinationLocationCode": get_iata_code(form.cleaned_data["destination"]),
                "departureDate": form.cleaned_data["departure_date"].strftime("%Y-%m-%d"),
                "returnDate": form.cleaned_data["return_date"].strftime("%Y-%m-%d"),
                "adults": int(form.cleaned_data["adults"]),
                "travelClass": form.cleaned_data["class_type"],
            }
            return render(
                request, "search.html", {"form": form, "flight_offers": get_flight_offers(**kwargs)}
            )


def get_flight_offers(**kwargs) -> list[dict]:
    search_flights = amadeus.shopping.flight_offers_search.get(**kwargs)
    flight_offers = []
    # fmt: off
    # search_flights = [{'type': 'flight-offer', 'id': '1', 'source': 'GDS', 'instantTicketingRequired': False, 'nonHomogeneous': False, 'oneWay': False, 'lastTicketingDate': '2023-09-29', 'lastTicketingDateTime': '2023-09-29', 'numberOfBookableSeats': 9, 'itineraries': [{'duration': 'PT9H25M', 'segments': [{'departure': {'iataCode': 'MAD', 'terminal': '4S', 'at': '2024-02-02T11:55:00'}, 'arrival': {'iataCode': 'CCS', 'at': '2024-02-02T16:20:00'}, 'carrierCode': 'IB', 'number': '6673', 'aircraft': {'code': '332'}, 'operating': {'carrierCode': 'IB'}, 'duration': 'PT9H25M', 'id': '46', 'numberOfStops': 0, 'blacklistedInEU': False}]}, {'duration': 'PT8H35M', 'segments': [{'departure': {'iataCode': 'CCS', 'at': '2024-04-09T17:20:00'}, 'arrival': {'iataCode': 'MAD', 'terminal': '4S', 'at': '2024-04-10T07:55:00'}, 'carrierCode': 'IB', 'number': '6674', 'aircraft': {'code': '332'}, 'operating': {'carrierCode': 'IB'}, 'duration': 'PT8H35M', 'id': '115', 'numberOfStops': 0, 'blacklistedInEU': False}]}], 'price': {'currency': 'EUR', 'total': '801.94', 'base': '250.00', 'fees': [{'amount': '0.00', 'type': 'SUPPLIER'}, {'amount': '0.00', 'type': 'TICKETING'}], 'grandTotal': '801.94', 'additionalServices': [{'amount': '180.00', 'type': 'CHECKED_BAGS'}]}, 'pricingOptions': {'fareType': ['PUBLISHED'], 'includedCheckedBagsOnly': False}, 'validatingAirlineCodes': ['IB'], 'travelerPricings': [{'travelerId': '1', 'fareOption': 'STANDARD', 'travelerType': 'ADULT', 'price': {'currency': 'EUR', 'total': '801.94', 'base': '250.00'}, 'fareDetailsBySegment': [{'segmentId': '46', 'cabin': 'ECONOMY', 'fareBasis': 'QNL0NQB6', 'brandedFare': 'BASIC', 'class': 'Q', 'includedCheckedBags': {'quantity': 0}}, {'segmentId': '115', 'cabin': 'ECONOMY', 'fareBasis': 'QNL0NQB6', 'brandedFare': 'BASIC', 'class': 'Q', 'includedCheckedBags': {'quantity': 0}}]}]}, {'type': 'flight-offer', 'id': '2', 'source': 'GDS', 'instantTicketingRequired': False, 'nonHomogeneous': False, 'oneWay': False, 'lastTicketingDate': '2023-09-29', 'lastTicketingDateTime': '2023-09-29', 'numberOfBookableSeats': 9, 'itineraries': [{'duration': 'PT9H20M', 'segments': [{'departure': {'iataCode': 'MAD', 'terminal': '1', 'at': '2024-02-02T16:10:00'}, 'arrival': {'iataCode': 'CCS', 'at': '2024-02-02T20:30:00'}, 'carrierCode': 'UX', 'number': '71', 'aircraft': {'code': '787'}, 'operating': {'carrierCode': 'UX'}, 'duration': 'PT9H20M', 'id': '39', 'numberOfStops': 0, 'blacklistedInEU': False}]}, {'duration': 'PT8H40M', 'segments': [{'departure': {'iataCode': 'CCS', 'at': '2024-04-09T21:40:00'}, 'arrival': {'iataCode': 'MAD', 'terminal': '1', 'at': '2024-04-10T12:20:00'}, 'carrierCode': 'UX', 'number': '72', 'aircraft': {'code': '788'}, 'operating': {'carrierCode': 'UX'}, 'duration': 'PT8H40M', 'id': '116', 'numberOfStops': 0, 'blacklistedInEU': False}]}], 'price': {'currency': 'EUR', 'total': '922.69', 'base': '365.00', 'fees': [{'amount': '0.00', 'type': 'SUPPLIER'}, {'amount': '0.00', 'type': 'TICKETING'}], 'grandTotal': '922.69', 'additionalServices': [{'amount': '242.40', 'type': 'CHECKED_BAGS'}]}, 'pricingOptions': {'fareType': ['PUBLISHED'], 'includedCheckedBagsOnly': False}, 'validatingAirlineCodes': ['UX'], 'travelerPricings': [{'travelerId': '1', 'fareOption': 'STANDARD', 'travelerType': 'ADULT', 'price': {'currency': 'EUR', 'total': '922.69', 'base': '365.00'}, 'fareDetailsBySegment': [{'segmentId': '39', 'cabin': 'ECONOMY', 'fareBasis': 'QLYR6L', 'brandedFare': 'LITE', 'class': 'Q', 'includedCheckedBags': {'quantity': 0}}, {'segmentId': '116', 'cabin': 'ECONOMY', 'fareBasis': 'QLYR6L', 'brandedFare': 'LITE', 'class': 'Q', 'includedCheckedBags': {'quantity': 0}}]}]}]
    # fmt: on
    for flight in search_flights.data:
        offer = FlightProcessor(flight).get_flights()
        flight_offers.append([x.dict(x) for x in offer])
    return flight_offers


def get_iata_code(city_name):
    try:
        airport = Airport.objects.get(city=city_name)
        return airport.iata
    except Airport.DoesNotExist:
        print(f"No airport found for city '{city_name}'")
        return None
