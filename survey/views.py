from .models import Survey, Question
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import SurveySerializer, QuestionSerializer

# Create your views here.
#
class SurveyViewSet(viewsets.ModelViewSet):

    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    # def perform_create(self, serializer):


class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
