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

class SchoolView(generics.ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [permissions.AllowAny]
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

        response_final_score_dict = {
            "school_id": 0, 
            "student": [],
            "teacher": [],
            "parent": []
        }


        school_list = function.get_school_list(School,SchoolSerializer)

        school_list_with_result = []

        #获取每个学校
        for school in school_list:

            response_final_score_dict = {
            "school_id": school['id'], 
            "student": [],
            "teacher": [],
            "parent": []
        }
            #获取所有问卷 遍历每个问卷
            for survey in survey_list:
                
                if survey["school_id"] == school['id']:
              
                #获取问卷的所有回答

                    responses = function.get_responses_from_survey(survey) 

                    nested_dict = function.make_nested_dict(indicator_modules)

                    calculation_dict = function.add_score_to_nested_dict(nested_dict,responses)

                    #获取用于计算的字典
                    calculation_dict = function.add_weight_to_nested_dict(calculation_dict, indicator_modules)

                    #计算并获取最后分数
                    final_score_for_one_user = function.calculate_final_score(nested_dict)


                    # response_final_score_dict["school_id"] = survey["school_id"]

                    if responses:
                        if responses[0]["question"]["type"] == "S":
                            response_final_score_dict["student"].append(final_score_for_one_user)

                        elif responses[0]["question"]["type"] == "T":
                            response_final_score_dict["teacher"].append(final_score_for_one_user)

                        elif responses[0]["question"]["type"] == "P":
                            response_final_score_dict["parent"].append(final_score_for_one_user)

            school_list_with_result.append(response_final_score_dict)
        return Response(data=school_list_with_result, status=status.HTTP_200_OK)


