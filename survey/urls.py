from django.urls import path, include
from .views import QuestionView, SurveyView
urlpatterns = [
    path("questions/", QuestionView.as_view(), name='questions'),
    # path("answers/", ResponseView.as_view(), name='answers'),
    path("", SurveyView.as_view(), name='survey')
]
