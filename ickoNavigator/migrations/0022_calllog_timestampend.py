# Generated by Django 3.1.7 on 2022-07-07 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ickoNavigator', '0021_auto_20220707_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='calllog',
            name='timestampEnd',
            field=models.FloatField(null=True),
        ),
    ]
