from django.db import models

# @TODO: Analyze data better to set proper validators

class Region(models.Model):
    code = models.IntegerField()  # "Code Région" column in the CSV
    name = models.CharField(max_length=60)  # "Région" column in the CSV


class County(models.Model):
    code = models.CharField(max_length=2)  # "Code Département" column in the CSV
    name = models.CharField(max_length=60)  # "Département" column in the CSV
    region = models.ForeignKey('regions.Region', models.CASCADE, related_name='counties')


# @TODO depends on the needs of application split postal code to different table. Because some of them are multiple per commune. Example: 66000/66100 for PERPIGNAN
class City(models.Model):
    area = models.FloatField() # "Superficie" column in the CSV
    code_insee = models.CharField(max_length=5)  # "Code INSEE" columun in the CSV
    code_postal = models.IntegerField() # "Code Postal" column in the CSV
    county = models.ForeignKey('regions.County', models.CASCADE, related_name='cities')
    name = models.CharField(max_length=60) # "Commune" column in the CSV
    population = models.FloatField() # "Population" column in the CSV