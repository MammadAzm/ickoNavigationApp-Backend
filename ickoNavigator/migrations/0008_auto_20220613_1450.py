# Generated by Django 3.1.7 on 2022-06-13 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ickoNavigator', '0007_auto_20220613_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpsdata',
            name='timestamp',
            field=models.FloatField(),
        ),
    ]
