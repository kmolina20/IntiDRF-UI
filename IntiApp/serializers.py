from rest_framework import serializers
from .models import Activity, Version

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        field = '__all__'


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'