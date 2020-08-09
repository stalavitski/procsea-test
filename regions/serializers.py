from rest_framework import serializers

from regions.models import Region


class RegionSerializer(serializers.ModelSerializer):
    lat = serializers.CharField(read_only=True)
    lon = serializers.CharField(read_only=True)
    total_area = serializers.SerializerMethodField()
    total_population = serializers.SerializerMethodField()

    class Meta:
        exclude = ['id']
        model = Region

    def get_total_area(self, obj):
        return 0 if obj.area_sum is None else obj.area_sum

    def get_total_population(self, obj):
        population_sum = 0 if obj.population_sum is None else obj.population_sum
        return round(population_sum, 1)
