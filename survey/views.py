from .models import Survey, Question, Response
from rest_framework import generics, permissions
from .serializers import SurveySerializer, QuestionSerializer, ResponseSerializer

# Create your views here.


class QuestionView(generics.ListAPIView):

    serializer_class = QuestionSerializer

    def get_queryset(self):

        type = self.request.user.position
        return Question.objects.filter(type=type)


class SurveyView(generics.CreateAPIView):

    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def perform_create(self, serializer):
        user = self.request.user
        school = user.school
        
        serializer.save(school=school, user=user)

# class ResponseView(generics.ListCreateAPIView):

#     queryset = Response.objects.all()
#     serializer_class = ResponseSerializer

    # def get_queryset(self):

    #     type = self.request.user.position
        
    #     return Question.objects.filter(type=type)