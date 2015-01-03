# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0002_translater_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translater',
            name='nickname',
            field=models.CharField(unique=True, max_length=30),
            preserve_default=True,
        ),
    ]
