import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RankingSystem.settings")

import django

django.setup()

from survey.models import IndicatorI, IndicatorII, IndicatorIII, Question


def w_2_db_Ind1(file_name):
    f = open(file_name)

    for line in f:
        title, weight, blank = line.split('|')
        IndicatorI.objects.get_or_create(title=title, weight=weight)

    f.close()


def w_2_db_Ind2(file_name):
    f = open(file_name)

    for line in f:
        title, weight, upper_indicator_name, blank = line.split('|')

        IndI = IndicatorI.objects.filter(title=upper_indicator_name).first()
        IndicatorII.objects.get_or_create(title=title, weight=weight, IndicatorI=IndI)

    f.close()

def w_2_db_Ind3(file_name):
    f = open(file_name)

    for line in f:
        title, weight, upper_indicator_name, blank = line.split('|')
        IndII = IndicatorII.objects.filter(title=upper_indicator_name).first()
        IndicatorIII.objects.get_or_create(title=title, weight=weight, IndicatorII=IndII)

    f.close()

def w_2_db_Questions(file_name):
    f = open(file_name)

    for line in f:
        content, weight, category, upper_indicator_name, blank = line.split('|')
        IndIII = IndicatorIII.objects.filter(title=upper_indicator_name).first()
        Question.objects.get_or_create(content=content, weight=weight, type=category, indicatorIII=IndIII)

    f.close()

if __name__ == "__main__":

    while True:
        a = int(input('1-Indicator I\n2-Indicator II\n3-Indicator III\n4-Questions\n5-quit\n'))
        if a == 1:
            w_2_db_Ind1('./txt/indicators_1.txt')
            print('IMPORT INDICATOR1 DONE!')
        elif a == 2:
            w_2_db_Ind2('./txt/indicators_2.txt')
            print('IMPORT INDICATOR2 DONE!')
        elif a == 3:
            w_2_db_Ind3('./txt/indicators_3.txt')
            print('IMPORT INDICATOR3 DONE!')
        elif a == 4:
            w_2_db_Questions('./txt/questions.txt')
            print('IMPORT QUESTIONS DONE!')
        elif a == 5:
            break
