# Generated by Django 3.1 on 2020-08-08 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='area',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='city',
            name='code_postal',
            field=models.CharField(max_length=60),
        ),
    ]
