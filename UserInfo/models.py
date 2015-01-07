from django.db import models
from django.contrib import admin
from django.contrib.auth.models import *

# Create your models here.
class TranslaterManager(models.Manager):
    def create_translator(self, nickname, active, user):
        translator = self.model(nickname=nickname, active=active)
        translator.user = user
        translator.save()
        return translator

class Translater(models.Model):
    user = models.OneToOneField(User)
    active = models.IntegerField()
    username = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    phone2 = models.CharField(max_length=30)
    phone3 = models.CharField(max_length=30)
    bank = models.CharField(max_length=30)
    bank_num = models.CharField(max_length=70)
    service_available = models.CommaSeparatedIntegerField(max_length=50)
    language_available = models.CommaSeparatedIntegerField(max_length=50)
    translate_available = models.CommaSeparatedIntegerField(max_length=50)
    school = models.TextField()
    career = models.TextField()
    major = models.CharField(max_length=30)
    lang_experience = models.TextField()
    alarmOn = models.BooleanField(default=False)
    udidiOS = models.CharField(max_length = 200)
    udidand = models.CharField(max_length = 200)

    objects = TranslaterManager()

    def __str__(self):
        return self.nickname

class TranslaterAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'nickname', 'active', 'phone', 'phone2', 'phone3', 'bank', 'bank_num', 'service_available', 'language_available', 'translate_available', 'school', 'career', 'lang_experience', 'alarmOn', 'udidiOS', 'udidand')
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
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=30)
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