# Generated by Django 4.2.6 on 2023-11-13 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_exerciseset'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseset',
            name='order',
            field=models.IntegerField(),
            preserve_default=False,
        ),
    ]