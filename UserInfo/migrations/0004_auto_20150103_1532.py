# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0003_auto_20150103_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translater',
            name='nickname',
            field=models.CharField(max_length=30),
            preserve_default=True,
        ),
    ]
