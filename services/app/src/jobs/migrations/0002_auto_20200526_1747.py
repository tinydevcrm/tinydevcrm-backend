# Generated by Django 3.0.4 on 2020-05-26 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cronjob',
            name='job_id',
            field=models.IntegerField(unique=True),
        ),
    ]
