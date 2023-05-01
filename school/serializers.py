from .models import School
from rest_framework import serializers


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    surveys = serializers.StringRelatedField(many=True,
                                             read_only=True,
                                             )

    class Meta:
        model = School
        fields = '__all__'
