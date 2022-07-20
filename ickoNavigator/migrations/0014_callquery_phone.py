# Generated by Django 3.1.7 on 2022-07-02 14:19

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('ickoNavigator', '0013_callquery'),
    ]

    operations = [
        migrations.AddField(
            model_name='callquery',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+980000000000', max_length=128, region=None, unique=True),
        ),
    ]
