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
    translater = models.ForeignKey(Translater, null=True)
    originallang = models.IntegerField()
    changedlang = models.IntegerField()
    period = models.IntegerField()
    register_date = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    price = models.IntegerField(null=True)

    objects = OrderManager()

    def __str__(self):
        return self.customer.nickname + "to" + self.customer.nickname


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'get_customer', 'get_translater', 'originallang', 'changedlang', 'period', 'filename', 'register_date')
    def get_customer(self, obj):
        return obj.customer.nickname
    def get_translater(self, obj):
        if obj.translater is not None :
            return obj.translater.nickname
        else :
            return ''
admin.site.register(Order, OrderAdmin)
