# Generated by Django 3.1.7 on 2022-07-14 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ickoNavigator', '0025_loading_paveddistance'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Temp',
        ),
        migrations.RenameField(
            model_name='loading',
            old_name='responsibleMachine',
            new_name='responsibleMachineID',
        ),
    ]