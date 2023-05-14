from django.db import models

# Create your models here.
class School(models.Model):

    name = models.CharField(max_length=256, null=False)
    city = models.CharField(max_length=256, null=True, blank=True)
    is_national = models.BooleanField(null=True, blank=True, default=True)
    types = models.CharField(max_length=256, null=True, blank=True)
    language = models.CharField(max_length=256, null=True, blank=True)
    max_year = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self): 
        return self.name 

class Result(models.Model):

    score = models.FloatField(default=0)
    indicatorI = models.ForeignKey('survey.IndicatorI', on_delete=models.CASCADE)
    school_id = models.ForeignKey('School', on_delete=models.CASCADE)
