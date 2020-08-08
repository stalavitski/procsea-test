from rest_framework import mixins, viewsets

from regions.models import Region
from regions.serializers import RegionSerializer


class RegionView(mixins.ListModelMixin, viewsets.GenericViewSet):
    http_method_names = ['get', 'head']
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
