from .models import School
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import SchoolSerializer

# Create your views here.
#
class SchoolViewSet(viewsets.ModelViewSet):

    queryset = School.objects.all()
    serializer_class = SchoolSerializer
#
#     def get(self, request):
#         print('Hello im get')
#
#     def post(self, request):
#         print('Im POST')


