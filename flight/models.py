from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Airport(models.Model):
    iata = models.CharField(max_length=3)
    icao = models.CharField(max_length=4)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.iata} - {self.icao} - {self.name} ({self.city} - {self.country})"
