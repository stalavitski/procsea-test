import requests
from django.db import models

# @TODO: Analyze data better to set proper validators

class Region(models.Model):
    coordinates = None

    code = models.IntegerField()  # "Code Région" column in the CSV
    name = models.CharField(max_length=60)  # "Région" column in the CSV

    def __str__(self):
        return '{}: {}, {}'.format(self.pk, self.code, self.name)

    def __repr__(self):
        return '{}: {}, {}'.format(self.pk, self.code, self.name)

    def get_coordinates(self):
        """
        Retrieves coordinates from external API and stores in attribute.
        :return: dict of lat/lon coordinates
        """
        if self.coordinates is None:
            url = 'https://nominatim.openstreetmap.org/search?country=France&state={}&format=json'.format(self.name)
            response = requests.get(url)
            self.coordinates = {
                'lat': None,
                'lon': None
            }

            if response.status_code == 200 and len(response.json()):
                location = response.json().pop()

                self.coordinates = {
                    'lat': location['lat'],
                    'lon': location['lon']
                }

        return self.coordinates

    @property
    def lat(self):
        coordinates = self.get_coordinates()
        return coordinates['lat']

    @property
    def lon(self):
        coordinates = self.get_coordinates()
        return coordinates['lon']


class County(models.Model):
    code = models.CharField(max_length=2)  # "Code Département" column in the CSV
    name = models.CharField(max_length=60)  # "Département" column in the CSV
    region = models.ForeignKey('regions.Region', models.CASCADE, related_name='counties')

    def __str__(self):
        return '{}: {}, {}'.format(self.pk, self.code, self.name)

    def __repr__(self):
        return '{}: {}, {}'.format(self.pk, self.code, self.name)


# @TODO depends on the needs of application split postal code to different table. Because some of them are multiple per commune. Example: 66000/66100 for PERPIGNAN
class City(models.Model):
    area = models.IntegerField() # "Superficie" column in the CSV
    code_insee = models.CharField(max_length=5)  # "Code INSEE" columun in the CSV
    code_postal = models.CharField(max_length=60) # "Code Postal" column in the CSV
    county = models.ForeignKey('regions.County', models.CASCADE, related_name='cities')
    name = models.CharField(max_length=60) # "Commune" column in the CSV
    population = models.FloatField() # "Population" column in the CSV

    def __str__(self):
        return '{}: {}, {}'.format(self.pk, self.code_insee, self.name)

    def __repr__(self):
        return '{}: {}, {}'.format(self.pk, self.code_insee, self.name)
