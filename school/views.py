from .models import School
from rest_framework.views import APIView
from rest_framework import permissions, generics, status
from .serializers import SchoolSerializer, ResultSerializer
from rest_framework.response import Response
from utils.functions import Function
from survey.models import Survey, Question, IndicatorI, IndicatorII, IndicatorIII
from survey.serializers import SurveySerializer, ResponseSerializer, QuestionSerializer
from django.db.models import Max
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.serializers import UserSerializer

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
    queryset = School.objects.filter(is_active=True)
    serializer_class = SchoolSerializer
    permission_classes = [permissions.AllowAny]

class SchoolRequestView(generics.ListCreateAPIView):
    queryset = School.objects.filter(is_active=False)
    serializer_class = SchoolSerializer
    permission_classes = [permissions.AllowAny]


class ResultView(APIView):

    authentication_classes = [JWTAuthentication,]
    permission_classes=[permissions.AllowAny]
    

    def get(self, request):
        function = Function()

        survey_serializer = SurveySerializer
        survey_list = function.get_all_survey(Survey, survey_serializer)


             
        indicator_modules = {
                            "Ind1":IndicatorI,
                            "Ind2": IndicatorII,
                            "Ind3": IndicatorIII,
                            "Question": Question
                            }

         
        

        response_final_score_dict = {
            "school_id": 0, 
            "user": [],
        }


        school_list = function.get_school_list(School,SchoolSerializer)

        school_list_with_result = []

        #获取每个学校
        for school in school_list:

            response_final_score_dict = {
            "school": SchoolSerializer(school).data , 
            "user": [],
            # "teacher": [],
            # "parent": []
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


                    if responses:
                        # if responses[0]["question"]["type"] == "S":
                        response_final_score_dict["user"].append(final_score_for_one_user)

                        # elif responses[0]["question"]["type"] == "T":
                            # response_final_score_dict["teacher"].append(final_score_for_one_user)

                        # elif responses[0]["question"]["type"] == "P":
                        #     response_final_score_dict["parent"].append(final_score_for_one_user)


            school_list_with_result.append(response_final_score_dict)


        school_unsorted_by_score_list = []
        # 遍历学校结果添加到数组
        for school_result in school_list_with_result:
            school_unsorted_by_score_list.append(function.calculate_average(school_result))

        #获取所有学校的评分平均数
        C = function.get_all_schools_avg(school_unsorted_by_score_list)
        
        # 添加bayes分数
        for school in school_unsorted_by_score_list:
            school['bayes_result'] = function.bayes_theorem(school, C)
        
        # 使用sorted()函数进行排序
        school_sorted_by_score_list = sorted(
            school_unsorted_by_score_list, key=lambda x: x['bayes_result'], reverse=True)
        
        # 添加排名
        for i, d in enumerate(school_sorted_by_score_list, start=1):
            d['rank'] = i

        #检查是否订阅
        user = request.user
        print('###########', user, user.is_authenticated)
        if user.is_authenticated:
            user_data = UserSerializer(user).data
            for school in school_sorted_by_score_list:
                # print(' user_data[subscription]: ',  user_data['subscription'])
                # print('school[school][id]: ', school['school']['id'])
                if user_data['subscription']:
                    for subs in user_data['subscription']:
                        # print(type(school['school']['id']), type(subs['school_id']))
                        if school['school']['id'] == subs['school_id']:
                            school['favorite'] = { 'is_favorite': True, 'favorite_id': subs['id'] }
                        else:
                            school['favorite'] = { 'is_favorite': False }
                else:
                    school['favorite'] = { 'is_favorite': False }
                    
        else:
            for school in school_sorted_by_score_list:
                school['favorite'] = { 'is_favorite': False }
            
        #计算最晚时间
        latest_post = Survey.objects.all().aggregate(Max('post_time'))['post_time__max']
        
        return Response(data={'ranking':school_sorted_by_score_list,
        'latest_post_time': latest_post}, status=status.HTTP_200_OK)


