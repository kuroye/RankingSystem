from django.urls import path
from .views import ResultView, CategoryCountView, SchoolView
urlpatterns = [
    path("results/", ResultView.as_view(), name='results'),
    path("counts/", CategoryCountView.as_view(), name='counts'),
    path("", SchoolView.as_view(), name='schools')
    # path("answers/", ResponseView.as_view(), name='answers'),
    # path("", SurveyView.as_view(), name='survey')
]