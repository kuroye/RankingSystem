# Generated by Django 4.1.5 on 2023-01-11 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0001_initial"),
        ("school", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="IndicatorI",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=128, null=True)),
                ("weight", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="IndicatorII",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=128, null=True)),
                ("weight", models.FloatField()),
                (
                    "IndicatorI",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="survey.indicatori",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IndicatorIII",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=128, null=True)),
                ("weight", models.FloatField()),
                (
                    "IndicatorII",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="survey.indicatorii",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(null=True)),
                ("weight", models.FloatField(default=0.1)),
                (
                    "indicatorIII",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="survey.indicatoriii",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Survey",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.FloatField()),
                (
                    "question_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="survey.question",
                    ),
                ),
                (
                    "school_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="school.school"
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.user"
                    ),
                ),
            ],
        ),
    ]
