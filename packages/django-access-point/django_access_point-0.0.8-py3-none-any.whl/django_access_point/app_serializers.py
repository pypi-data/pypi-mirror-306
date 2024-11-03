from rest_framework import serializers

from .models import User, UserCustomField, UserCustomFieldValue

class CustomFieldValueSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserCustomFieldValue
        fields = ['custom_field', 'value']

class CustomerSerializer(serializers.ModelSerializer):
    custom_field_values = CustomFieldValueSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'status', 'custom_field_values']
