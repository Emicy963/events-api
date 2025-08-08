from rest_framework import serializers
from .models import EventCategory


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        models = EventCategory
        fields = "all"
