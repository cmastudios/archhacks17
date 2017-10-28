# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-28 20:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nutritrack', '0002_auto_20171028_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutritrack.Meal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
