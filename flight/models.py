from django.db import models


class Airport(models.Model):
    iata = models.CharField(max_length=3)
    icao = models.CharField(max_length=4)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.iata} - {self.icao} - {self.name} ({self.city} - {self.country})"
