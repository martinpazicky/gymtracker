# Generated by Django 4.2.6 on 2023-10-20 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_exerciserealiation_exercise_body_part_workout_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='name',
            field=models.CharField(default='', max_length=40),
        ),
    ]
