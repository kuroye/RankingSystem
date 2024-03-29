# Generated by Django 4.1.5 on 2023-02-15 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_alter_user_position"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="phone_num",),
        migrations.RemoveField(model_name="user", name="username",),
        migrations.AddField(
            model_name="user",
            name="email",
            field=models.CharField(default="abcd", max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="fullname",
            field=models.CharField(default="abcd", max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user", name="password", field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name="user",
            name="position",
            field=models.CharField(
                choices=[
                    ("S", "School Student"),
                    ("T", "Teacher"),
                    ("P", "Parent"),
                    ("U", "Graduate"),
                ],
                max_length=1,
            ),
        ),
    ]
