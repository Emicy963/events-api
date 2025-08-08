from rest_framework import serializers
from .models import Event, EventCategory


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        models = EventCategory
        fields = "all"

class EventSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer(read_only=True)
    organizer_name = serializers.CharField(source="organizer.get_full_name", read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = [
            "organizer",
            "views_count",
            "tickets_sold",
            "revenue",
        ]
