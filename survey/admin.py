from django.contrib import admin
from .models import IndicatorI, IndicatorII, IndicatorIII, Question, Survey

# Register your models here.
admin.site.register(IndicatorI)
admin.site.register(IndicatorII)
admin.site.register(IndicatorIII)
admin.site.register(Question)
admin.site.register(Survey)
