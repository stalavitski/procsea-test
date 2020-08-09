from django.test import TestCase
from rest_framework.test import APIRequestFactory
import json

from regions.views import RegionView


class RegionViewTestCase(TestCase):
    fixtures = ['0001_regions.json', '0002_counties.json', '0003_cities.json']

    def _get_api_response(self):
        factory = APIRequestFactory()
        view = RegionView.as_view({'get': 'list'})
        request = factory.get('/api/regions/')
        return view(request)

    # total_area tests
    def test__total_area__calculates_correctly(self):
        # Act
        response = self._get_api_response()
        data = json.loads(response.rendered_content.decode('utf-8'))
        region_data = data['results'][0]
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(region_data['totalArea'], 6)

    # total_population tests
    def test__total_population__calculates_correctly(self):
        # Act
        response = self._get_api_response()
        data = json.loads(response.rendered_content.decode('utf-8'))
        region_data = data['results'][0]
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(region_data['totalPopulation'], 60)
