from .models import Survey, Question, IndicatorIII, Response, IndicatorII, IndicatorI
from rest_framework import serializers
from user.serializers import UserSerializer
from school.serializers import SchoolSerializer


class IndicatorISerializer(serializers.ModelSerializer):

    class Meta:
        model = IndicatorI
        fields = ['id', 'title', 'weight']
    

class IndicatorIISerializer(serializers.ModelSerializer):
    
    Indicator1 = serializers.SerializerMethodField()
    
    class Meta:
        model = IndicatorII  
        fields = ['id', 'title', 'weight', 'IndicatorI']

    def to_representation(self, instance):

        indicator1 = IndicatorI.objects.filter(pk=instance.IndicatorI.id).first()

        # print(indicator1)
        indicator1_data = IndicatorISerializer(indicator1).data


        return {
                'indicator2_id': instance.id,
                'title': instance.title,
                'weight': instance.weight,
                'indicator1': indicator1_data
        }

class IndicatorIIISerializer(serializers.ModelSerializer):

    class Meta:
        model = IndicatorIII
        fields = ['id', 'title', 'weight', 'IndicatorII']

    def to_representation(self, instance):

        indicator2 = IndicatorII.objects.filter(pk=instance.IndicatorII.id)

        indicator2_data = IndicatorIISerializer(indicator2, many=True).data[0]


        return {
                'indicator3_id': instance.id,
                'title': instance.title,
                'weight': instance.weight,
                'indicator2': indicator2_data
        }

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'content', 'weight', 'type', 'indicatorIII']


    
    def to_representation(self, instance):

        indicator3 = IndicatorIII.objects.filter(pk=instance.indicatorIII.id)

        indicator3_data = IndicatorIIISerializer(indicator3, many=True).data[0]


        return {
                'question_id': instance.id,
                'content': instance.content,
                'weight': instance.weight,
                'type': instance.type,
                'indicator3': indicator3_data
        }

# Response has Question
class ResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Response
        fields = ['id', 'score', 'survey_id', 'question']

    def to_representation(self, instance):

        question = Question.objects.filter(pk=instance.question.id)

        question_data = QuestionSerializer(question, many=True).data[0]

        return {'response_id': instance.id,
                'survey_id': instance.survey.id,
                'score': instance.score,
                'question': question_data,
                }

# Survey has Response   Survey>Response
class SurveySerializer(serializers.ModelSerializer):

    responses = ResponseSerializer(many=True) 


    class Meta:
        model = Survey
        fields = ['id', 'user', 'school', 'responses' ]
        read_only_fields = ['id', 'user', 'school']
        

    def to_representation(self, instance):

        responses = Response.objects.filter(survey=instance).all()

        response_data = ResponseSerializer(responses, many=True).data

        # print(dir(response_data))
        return {
            'survey_id': instance.id,
            'user_id': instance.user.id,
            'school_id': instance.school.id,
            'responses': response_data
        }
        # return super().to_representation(instance)

        
        # return super().to_representation(instance)


    # 返回Survey 这是SurveySerializer
    def create(self, validated_data):

        if validated_data.get('school') is None:
            raise serializers.ValidationError({"error": "There is no school"})

        #拿到了responses数组
        responses_data = validated_data.pop('responses')
        survey = Survey.objects.create(**validated_data)

            
        for response_data in responses_data:

            Response.objects.create(survey=survey, **response_data)

        survey.responses = responses_data
        return survey


