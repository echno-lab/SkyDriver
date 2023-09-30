import ast
import os

import requests
from amadeus import Client, ResponseError
from django.shortcuts import get_object_or_404, redirect, render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from flight.flight_offer import FlightProcessor
from skydriver import settings
from skydriver.config import AMADEUS_API_KEY, AMADEUS_API_SECRET

from .forms import BookFlightForm, FlightSearchForm
from .models import Airport, Flight

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


def book_flight(request):
    if request.method == "POST":
        flights = ast.literal_eval(request.POST.get("flights"))
        response = []
        for flight in flights:
            data = {
                "first_departure_airport": flight["first_departure_airport"],
                "first_arrival_airport": flight["first_arrival_airport"],
                "first_departure_date": flight["first_departure_date"],
                "first_arrival_date": flight["first_arrival_date"],
                "first_airline": flight["first_airline"],
                "second_departure_airport": flight.get("second_departure_airport", None),
                "second_arrival_airport": flight.get("second_arrival_airport", None),
                "second_departure_date": flight.get("second_departure_date", None),
                "second_arrival_date": flight.get("second_arrival_date", None),
                "second_airline": flight.get("second_airline", None),
            }
            header = {"Authorization": f"Bearer {request.session['access_token']}"}
            response.append(requests.post(f"{settings.API_URL}flight/", headers=header, data=data))
        return redirect("tickets")
    else:
        return redirect("/")


def get_tickets(request):
    header = {"Authorization": f"Bearer {request.session['access_token']}"}
    response = requests.get(f"{settings.API_URL}flight/", headers=header)
    return render(request, "ticket.html", {"tickets": response.json()})


def delete_ticket(request):
    if request.method == "POST":
        header = {"Authorization": f"Bearer {request.session['access_token']}"}
        response = requests.delete(
            f"{settings.API_URL}flight/{request.POST.get('id')}", headers=header
        )
        if response.status_code == 204:
            return redirect("get_tickets")
        elif response.status_code == 401:
            return redirect("logout")
    else:
        return redirect("/")
