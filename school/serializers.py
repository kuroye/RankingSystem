from .models import School, Result
from rest_framework import serializers


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = '__all__'