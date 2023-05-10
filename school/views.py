from .models import School
from rest_framework.views import APIView
from rest_framework import permissions, generics, status
from .serializers import SchoolSerializer, ResultSerializer
from rest_framework.response import Response
from utils.functions import Function
from survey.models import Survey, Question, IndicatorI, IndicatorII, IndicatorIII
from survey.serializers import SurveySerializer, ResponseSerializer, QuestionSerializer
# Create your views here.
#
# class SchoolViewSet(viewsets.ModelViewSet):

#     queryset = School.objects.all()
#     serializer_class = SchoolSerializer
#
#     def get(self, request):
#         print('Hello im get')
#
#     def post(self, request):
#         print('Im POST')

class CategoryCountView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):

        schools_count = School.objects.all().count()

        categories = {
            'kindergardens':234,
            'schools':schools_count,
            'colleges':586,
            'universities':145,
            'clubs':214
        }
        return Response(data=categories, status=status.HTTP_200_OK)


class ResultView(APIView):

    # queryset = School.objects.all()
    # serializer_class = ResultSerializer
    permission_classes=[permissions.AllowAny]

    def get(self, request):
        function = Function()

        survey_serializer = SurveySerializer
        response_serializer = ResponseSerializer
        question_model = Question
        survey_list = function.get_all_survey(Survey, survey_serializer)
        result=[]

        #有好多问卷，遍历每个问卷
        for survey in survey_list:

            #一个问卷里有好多答案，从问卷里获取 这是一个人的回答
            responses = function.get_responses_from_survey(survey) 

            #遍历好多答案
            for response in responses:

                pass
                # #根据答案获取 分数 问题 占比

                # #回答分数
                # responsed_socre = function.get_score(response)
                # #问题
                # question = function.get_question(response)
                # #问题占比
                # question_weight = function.get_weight(question)

                # #单个问题相乘占比后的的分数
                # question_score = function.multiply_weight(
                #     responsed_socre,
                #     question_weight
                # )

                

                

                # result.append(question)
        # for survey in survey_list:

        #     responses = function.calculate_final_score(survey)
        #     indIII_score = []

        #     for response in responses.get('result'):

        #         indicator_III_score = (response.get('score')) * function.get_weight(
        #             question_model,response)
        #         indIII_score.append(indicator_III_score)

        #     result.append(indIII_score)
             
        indicator_modules = {
                            "Ind1":IndicatorI,
                            "Ind2": IndicatorII,
                            "Ind3": IndicatorIII,
                            "Question": Question
                            }

         
        
        nested_dict = function.make_nested_dict(indicator_modules)

        calculation_dict = function.add_score_to_nested_dict(nested_dict, survey_list[-1]["responses"])
        
        nested_dict = function.add_weight_to_nested_dict(calculation_dict, indicator_modules)
        mydict = function.calculate_final_score(nested_dict)
        
        return Response(data=mydict, status=status.HTTP_200_OK)


