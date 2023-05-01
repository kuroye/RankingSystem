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

    # level = models.CharField(max_length=1, null=False, choices=LEVEL)

    def __str__(self):
        # return self.name + ' | ' + self.level + ' | ' + str(self.weight*100) + '%'
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
        ('P', 'Parent'),
        ('U', 'Graduate')
    ]
    content = models.TextField(null=True)
    weight = models.FloatField(null=False, default=0.1)
    type = models.CharField(max_length=1, null=True, choices=TYPE)
    indicatorIII = models.ForeignKey('IndicatorIII', on_delete=models.CASCADE)

    def __str__(self):
        return self.content + ' | ' + self.type + ' | ' + str(self.weight * 100) + '%'


class Survey(models.Model):
    score = models.FloatField(null=False)

    school = models.ForeignKey('school.School', on_delete=models.CASCADE, null=True, related_name='school')
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, related_name='user')