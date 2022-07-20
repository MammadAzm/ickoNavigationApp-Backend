# Generated by Django 3.1.7 on 2022-07-14 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ickoNavigator', '0022_calllog_timestampend'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=15)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=15)),
                ('description', models.CharField(max_length=150)),
                ('enum_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ickoNavigator.enumeration')),
            ],
        ),
    ]