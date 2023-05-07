from .models import Survey, Question, IndicatorIII, Response
from rest_framework import serializers
from user.serializers import UserSerializer
from school.serializers import SchoolSerializer


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'score', 'question', 'survey_id']

class SurveySerializer(serializers.ModelSerializer):
    school = serializers.ReadOnlyField(source='school.id')
    user = serializers.ReadOnlyField(source='user.id')

    responses = ResponseSerializer(many=True)


    class Meta:
        model = Survey
        fields = ['id', 'user', 'school', 'responses' ]

    def to_representation(self, instance):

        resposes = Response.objects.filter(survey=instance)
        instance.responses = resposes

        return super().to_representation(instance)


    def create(self, validated_data):

        if validated_data.get('school') is None:
            raise serializers.ValidationError({"error": "There is no school"})

        responses_data = validated_data.pop('responses')
        survey = Survey.objects.create(**validated_data)

            
        for response_data in responses_data:

            Response.objects.create(survey=survey, **response_data)

        survey.responses = responses_data
        return survey


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'content', 'weight', 'type', 'indicatorIII']

class IndicatorIIISerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = IndicatorIII
        fields = ['url', 'id', 'title', 'weight']
