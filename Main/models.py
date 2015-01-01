from django.db import models
from django.contrib import admin
from UserInfo.models import Translater, Customer

# Create your models here.
class OrderManager(models.Manager):
    def create_order(self, type, status, customer, originallang, changedlang, period, filename):
        order = self.model(type=type, status=status, customer=customer, originallang=originallang, changedlang=changedlang, period=period, filename=filename)
        order.save()
        return order

class Order(models.Model):
    type = models.IntegerField()  #0:Translation
    status = models.IntegerField()
    customer = models.ForeignKey(Customer, null=True)
    translaters = models.ManyToManyField(Translater, null=True)
    originallang = models.IntegerField()
    changedlang = models.IntegerField()
    period = models.IntegerField()
    register_date = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    trans_filename = models.CharField(max_length=255)
    price = models.IntegerField(null=True)

    objects = OrderManager()

    def __str__(self):
        return self.customer.nickname + "to" + self.customer.nickname


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'get_customer', 'get_translaters', 'originallang', 'changedlang', 'period', 'filename', 'register_date')
    def get_customer(self, obj):
        return obj.customer.nickname
    def get_translaters(self, obj):
        text = ''
        for translater in obj.translaters.all():
            text = text + translater.nickname + ', '
        return text
admin.site.register(Order, OrderAdmin)


class MessageManager(models.Manager):
    def create_order(self, type, order, sender, receiver, content):
        order = self.model(type=type, order=order, sender=sender, receiver=receiver, content=content)
        order.save()
        return order

class Message(models.Model):
    type = models.IntegerField()
    order = models.ForeignKey(Order)
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    register_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    objects = MessageManager()

    def __str__(self):
        return self.sender + " to " + self.receiver

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'get_order', 'sender', 'receiver', 'content')
    def get_order(self, obj):
        return obj.order.id
admin.site.register(Message, MessageAdmin)


class TranslaterReviewManager(models.Manager):
    def create_review(self, reviewer, translater, content):
        review = self.model(reviewer=reviewer, translater=translater, content=content)
        review.save()
        return review

class TranslaterReview(models.Model):
    reviewer = models.ForeignKey(Customer)
    translater = models.ForeignKey(Translater)
    content = models.TextField()
    objects = TranslaterReviewManager()

    def __str__(self):
        return self.reviewer.nickname + "to" + self.translater.nickname

class TranslaterReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_reviewer', 'get_translater', 'content')
    def get_reviewer(self, obj):
        return obj.reviewer.nickname
    def get_translater(self, obj):
        return obj.translater.nickname
admin.site.register(TranslaterReview, TranslaterReviewAdmin)





