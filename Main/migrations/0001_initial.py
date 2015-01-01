# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender', models.CharField(max_length=255)),
                ('receiver', models.CharField(max_length=255)),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
                ('trans_filename', models.CharField(max_length=255)),
                ('price', models.IntegerField(null=True)),
                ('customer', models.ForeignKey(to='UserInfo.Customer', null=True)),
                ('translaters', models.ManyToManyField(to='UserInfo.Translater', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TranslaterReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('reviewer', models.ForeignKey(to='UserInfo.Customer')),
                ('translater', models.ForeignKey(to='UserInfo.Translater')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='order',
            field=models.ForeignKey(to='Main.Order'),
            preserve_default=True,
        ),
    ]
