from .models import Survey, Question, IndicatorIII
from rest_framework import serializers
from user.serializers import UserSerializer
from school.serializers import SchoolSerializer

class SurveySerializer(serializers.ModelSerializer):
    # school_name = SchoolSerializer()
    # school_id = serializers.RelatedField(source='School.school', read_only=True)

    user = UserSerializer()
    school = SchoolSerializer()

    class Meta:
        model = Survey
        fields = ['url', 'id', 'score', 'question_id', 'user', 'school']
        # fields = '__all__'
        # read_only_fields = ('id', 'user')

class QuestionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Question
        fields = ['url', 'id', 'content', 'weight', ]

class IndicatorIIISerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = IndicatorIII
        fields = ['url', 'id', 'title', 'weight']
