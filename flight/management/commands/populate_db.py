import string
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from flight.models import Airport


class Command(BaseCommand):
    help = "Populate the database with initial data"

    def handle(self, *args, **options):
        # Populate the airports
        base_url = "https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_"
        self.stdout.write(self.style.WARNING("Inserting Airports..."))
        for letter in string.ascii_uppercase:
            url = base_url + letter
            html = urlopen(url)
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table", class_="wikitable")

            for row in table.find_all("tr")[1:]:
                cells = row.find_all("td")
                if len(cells) > 5:
                    iata = cells[0].text.strip()
                    icao = cells[1].text.strip()
                    name = cells[2].text.strip()
                    location = cells[3].text.strip()
                    if "," in location:
                        city, country = [x.strip().upper() for x in cells[3].text.split(",")[-2:]]
                    else:
                        city, country = "", location.strip().upper()
                    Airport.objects.get_or_create(
                        name=name,
                        iata=iata,
                        icao=icao,
                        city=city,
                        country=country,
                    )
        self.stdout.write(self.style.SUCCESS("Airports inserted successfully!"))
