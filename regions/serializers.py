from rest_framework import serializers

from regions.models import Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Region