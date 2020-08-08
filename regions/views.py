from django.db import models
from rest_framework import mixins, viewsets

from regions.models import Region
from regions.serializers import RegionSerializer


class RegionView(mixins.ListModelMixin, viewsets.GenericViewSet):
    http_method_names = ['get', 'head']
    queryset = Region.objects.annotate(
        area_sum=models.Sum('counties__cities__area'),
        population_sum=models.Sum('counties__cities__population')
    )
    serializer_class = RegionSerializer
