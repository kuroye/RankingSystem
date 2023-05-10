from django.db import models


# Create your models here.
class IndicatorI(models.Model):
    # LEVEL = [
    #     ('1', 'I'),
    #     ('2', 'II'),
    #     ('3', 'III'),
    # ]
    title = models.CharField(max_length=128, null=True)
    weight = models.FloatField(null=False)


    def __str__(self):
        return self.title + ' | ' + str(self.weight * 100) + '%'


class IndicatorII(models.Model):
    title = models.CharField(max_length=128, null=True)
    weight = models.FloatField(null=False)
    IndicatorI = models.ForeignKey('IndicatorI', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title + ' | ' + str(self.weight * 100) + '%'


class IndicatorIII(models.Model):
    title = models.CharField(max_length=128, null=True)
    weight = models.FloatField(null=False)
    IndicatorII = models.ForeignKey('IndicatorII', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title + ' | ' + str(self.weight * 100) + '%'


class Question(models.Model):
    TYPE = [
        ('S', 'School Student'),
        ('T', 'Teacher'),
        ('P', 'Parent')
    ]
    content = models.TextField(null=True)
    weight = models.FloatField(null=False, default=0.1)
    type = models.CharField(max_length=1, null=True, choices=TYPE)
    indicatorIII = models.ForeignKey('IndicatorIII', on_delete=models.CASCADE)

    def __str__(self):
        return self.content + ' | ' + self.type + ' | ' + str(self.weight * 100) + '%'


class Survey(models.Model):
    
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, null=True, related_name='school')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, related_name='user')

class Response(models.Model):

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    score = models.FloatField(null=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)