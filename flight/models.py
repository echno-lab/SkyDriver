from django.contrib.auth.models import User
from django.db import models


class Airport(models.Model):
    iata = models.CharField(max_length=3)
    icao = models.CharField(max_length=4)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.iata} - {self.icao} - {self.name} ({self.city} - {self.country})"


class Flight(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    first_departure_airport = models.CharField(max_length=100)
    first_arrival_airport = models.CharField(max_length=100)
    first_departure_date = models.CharField(max_length=100)
    first_arrival_date = models.CharField(max_length=100)
    first_airline = models.CharField(max_length=100)
    second_departure_airport = models.CharField(max_length=100, blank=True, null=True)
    second_arrival_airport = models.CharField(max_length=100, blank=True, null=True)
    second_departure_date = models.CharField(max_length=100, blank=True, null=True)
    second_arrival_date = models.CharField(max_length=100, blank=True, null=True)
    second_airline = models.CharField(max_length=100, blank=True, null=True)
