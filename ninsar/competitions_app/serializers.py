from rest_framework import serializers
from .models import FlightScenario

class CompetitionRequestSerializer(serializers.Serializer):
    competition = serializers.CharField(max_length=128, label="Соревнование")
    user_name = serializers.CharField(max_length=150, label="Пользователь")
    scenario = serializers.ChoiceField(choices=FlightScenario.choices, label="Сценарий")


class ResultSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    user_name = serializers.CharField()
    flight_time = serializers.FloatField()
    command_name = serializers.CharField()


class CompetitionResponseSerializer(serializers.Serializer):
    user_result = ResultSerializer()
    other_results = ResultSerializer(many=True)