# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField()),
                ('status', models.IntegerField()),
                ('originallang', models.IntegerField()),
                ('changedlang', models.IntegerField()),
                ('period', models.IntegerField()),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('filename', models.CharField(max_length=255)),
                ('customer', models.ForeignKey(to='UserInfo.Customer', null=True)),
                ('translater', models.ForeignKey(to='UserInfo.Translater', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
