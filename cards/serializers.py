from rest_framework import serializers
from .models import Card
import re

class CardValidationSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    ccv = serializers.IntegerField()

    def validate_card_number(self, value):
        if len(value) != 16 or not re.match(r'^\d{16}$', value):
            raise serializers.ValidationError("Card number must be 16 digits.")
        return value

    def validate_ccv(self, value):
        if value < 100 or value > 999:
            raise serializers.ValidationError("CCV must be a three-digit number between 100 and 999.")
        return value

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'user', 'title', 'censored_number', 'is_valid', 'created_at']
        read_only_fields = ['user', 'is_valid', 'censored_number', 'created_at']
