# Generated by Django 4.2.6 on 2023-10-23 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_workout_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='routine',
            field=models.CharField(default='no', max_length=50),
        ),
    ]