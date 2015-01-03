from django.db import models
from django.contrib import admin
from django.contrib.auth.models import *

# Create your models here.
class TranslaterManager(models.Manager):
    def create_translator(self, nickname, active, workhours, detailExplanation, email, alarmOn, udidiOS, udidand, user):
        translator = self.model(nickname=nickname, active=active, workhours=workhours, detailExplanation=detailExplanation, email=email, alarmOn=alarmOn, udidiOS=udidiOS, udidand=udidand)
        translator.user = user
        translator.save()
        return translator

class Translater(models.Model):
    nickname = models.CharField(max_length = 30)
    active = models.BooleanField()
    user = models.OneToOneField(User)
    workhours = models.IntegerField()
    detailExplanation = models.TextField()
    email = models.CharField(max_length = 30)
    alarmOn = models.BooleanField(default=None)
    udidiOS = models.CharField(max_length = 200)
    udidand = models.CharField(max_length = 200)

    objects = TranslaterManager()

    def __str__(self):
        return self.nickname

class TranslaterAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'active', 'workhours', 'detailExplanation', 'email', 'udidiOS', 'udidand', 'get_user')
    def get_user(self, obj):
        return obj.user.username
admin.site.register(Translater, TranslaterAdmin)


class CustomerManager(models.Manager):
    def create_customer(self, nickname, imageURL, alarmOn, udidiOS, udidand, user):
        customer = self.model(nickname=nickname, imageURL=imageURL, alarmOn=alarmOn, udidiOS=udidiOS, udidand=udidand)
        customer.user = user
        customer.save()
        return customer

class Customer(models.Model):
    nickname = models.CharField(max_length = 30)
    user = models.OneToOneField(User)
    imageURL = models.CharField(max_length = 255)
    alarmOn = models.BooleanField(default=None)
    udidiOS = models.CharField(max_length = 200)
    udidand = models.CharField(max_length = 200)
    objects = CustomerManager()

    def __str__(self):
        return self.nickname

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'imageURL', 'alarmOn', 'udidiOS', 'udidand', 'get_user')
    def get_user(self, obj):
        return obj.user.username
admin.site.register(Customer, CustomerAdmin)

class TranslateScore(models.Model):
    score = models.IntegerField()