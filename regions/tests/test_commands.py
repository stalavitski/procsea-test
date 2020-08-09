from django.test import TestCase

from regions.management.commands.importregions import Command
from regions.models import City, County, Region


class MockReader:
    line_num = 1


class ImportRegionsCommandTestCase(TestCase):
    command = 'importregions'

    def _get_row(self, **kwargs):
        return [
            kwargs.get('code_insee'),
            kwargs.get('code_postal'),
            kwargs.get('city_name'),
            kwargs.get('county_name'),
            kwargs.get('region_name'),
            None,
            None,
            kwargs.get('area'),
            kwargs.get('population'),
            None,
            None,
            None,
            None,
            None,
            None,
            kwargs.get('county_code'),
            kwargs.get('region_code')
        ]

    # handle_row tests
    def test__handle_row__writes_data_to_the_model(self):
        # Arrange
        data = {
            'code_insee': 'insee',
            'code_postal': 'postal',
            'city_name': 'city_name',
            'county_name': 'county_name',
            'region_name': 'region_name',
            'area': 1,
            'population': 2,
            'county_code': '3',
            'region_code': 4
        }
        row = self._get_row(**data)
        command = Command()
        # Act
        command.handle_row(MockReader(), row)
        # Assert
        region = Region.objects.first()
        self.assertEqual(region.code, data['region_code'])
        self.assertEqual(region.name, data['region_name'])
        county = County.objects.first()
        self.assertEqual(county.code, data['county_code'])
        self.assertEqual(county.name, data['county_name'])
        self.assertEqual(county.region.id, region.id)
        city = City.objects.first()
        self.assertEqual(city.area, data['area'])
        self.assertEqual(city.code_insee, data['code_insee'])
        self.assertEqual(city.code_postal, data['code_postal'])
        self.assertEqual(city.county.id, county.id)
        self.assertEqual(city.name, data['city_name'])
        self.assertEqual(city.population, data['population'])

    def test__handle_row__skips_line__on_type_error(self):
        # Arrange
        command = Command()
        row = self._get_row()
        # Act
        command.handle_row(MockReader(), row)
        # Assert
        self.assertEqual(Region.objects.count(), 0)
        self.assertEqual(County.objects.count(), 0)
        self.assertEqual(City.objects.count(), 0)

    def test__handle_row__skips_line__on_index_error(self):
        # Arrange
        command = Command()
        # Act
        command.handle_row(MockReader(), [])
        # Assert
        self.assertEqual(Region.objects.count(), 0)
        self.assertEqual(County.objects.count(), 0)
        self.assertEqual(City.objects.count(), 0)

    def test__handle_row__skips_line__on_value_error(self):
        # Arrange
        command = Command()
        data = {
            'code_insee': 'insee',
            'code_postal': 'postal',
            'city_name': 'city_name',
            'county_name': 'county_name',
            'region_name': 'region_name',
            'area': 1,
            'population': 2,
            'county_code': '3',
            'region_code': 'test'
        }
        row = self._get_row(**data)
        # Act
        command.handle_row(MockReader(), row)
        # Assert
        self.assertEqual(Region.objects.count(), 0)
        self.assertEqual(County.objects.count(), 0)
        self.assertEqual(City.objects.count(), 0)

    # parse_csv tests
    def test__parse_csv__skips__if_file_is_missing(self):
        # Arrange
        command = Command()
        # Act
        command.parse_csv('error.csv')
        # Assert
        self.assertEqual(Region.objects.count(), 0)
        self.assertEqual(County.objects.count(), 0)
        self.assertEqual(City.objects.count(), 0)

    def test__parse_csv__adds_records(self):
        # Arrange
        command = Command()
        # Act
        command.parse_csv('test.csv')
        # Assert
        self.assertEqual(Region.objects.count(), 1)
        self.assertEqual(County.objects.count(), 1)
        self.assertEqual(City.objects.count(), 1)
