from django.urls import path
from .views import ResultView, CategoryCountView, SchoolView, SchoolRequestView
urlpatterns = [
    path("results/", ResultView.as_view(), name='results'),
    path("counts/", CategoryCountView.as_view(), name='counts'),
    path("", SchoolView.as_view(), name='schools'),
    path("request/", SchoolRequestView.as_view(), name='school requests')
]