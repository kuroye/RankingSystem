from django.db import models

# Create your models here.
class School(models.Model):

    name = models.CharField(max_length=128, null=False)
    location = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self): 
        return self.name 

class Result(models.Model):

    score = models.FloatField(default=0)
    indicatorI = models.ForeignKey('survey.IndicatorI', on_delete=models.CASCADE)
    school_id = models.ForeignKey('School', on_delete=models.CASCADE)
