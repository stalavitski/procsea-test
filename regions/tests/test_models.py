from django.test import TestCase

from regions.models import Region


class RegionTestCase(TestCase):
    fixtures = ['0001_regions.json']

    # get_coordinates tests
    def test__get_coordinates__returns_empty_dict__on_unsuccessful_api_request(self):
        # Arrange
        region = Region.objects.first()
        region._coordinates_endpoint = 'https://nominatim.openstreetmap.org/404'
        # Act
        coordinates = region.get_coordinates()
        # Assert
        self.assertIsNone(coordinates['lat'])
        self.assertIsNone(coordinates['lon'])

    def test__get_coordinates__returns_empty_dict__on_empty_api_response(self):
        # Arrange
        region = Region.objects.first()
        region.name = 'SHOULD-NOT-BE-FOUND'
        # Act
        coordinates = region.get_coordinates()
        # Assert
        self.assertIsNone(coordinates['lat'])
        self.assertIsNone(coordinates['lon'])

    def test__get_coordinates__returns_filled_dict__on_successful_api_response(self):
        # Arrange
        region = Region.objects.first()
        region.name = 'Bretagne'
        # Act
        coordinates = region.get_coordinates()
        # Assert
        self.assertIsNotNone(coordinates['lat'])
        self.assertIsNotNone(coordinates['lon'])

    def test__get_coordinates__caches_data__after_api_call(self):
        # Arrange
        region = Region.objects.first()
        # Act
        region.get_coordinates()
        # Assert
        self.assertIsNotNone(region._coordinates)
