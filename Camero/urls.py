from django.conf.urls import patterns, include, url
from django.contrib import admin
from Main.views import *
from UserInfo.views import *

urlpatterns = patterns('',
    #web
    url(r'^$', main_page, name='main_page'),
    url(r'^myinfo_page/', myinfo_page),
    url(r'^budget_admin_page/', budget_admin_page, name="admin_page"),
    url(r'^update_translater/', update_translater),

    #status
    url(r'^calculate_budget/', calculate_budget),
    url(r'^makestatus/', makestatus),
    url(r'^mystatus/(?P<order_id>\d+)/', mystatus, name='mystatus'),
    url(r'^translater_mystatus/(?P<order_id>\d+)/', translater_mystatus, name='translater_mystatus'),
    url(r'^make_order_message', make_order_message),

    # user
    url(r'^customer_register_user/', customer_register_user),
    url(r'^translater_register_user/', translater_register_user),
    url(r'^login_user/', login_user),
    url(r'^logout_user/', logout_user),
    url(r'^register_order/', register_order),
    url(r'^update_order/(?P<status>\d+)/', update_order),


    # url(r'^TranslateWeb/', include('TranslateWeb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
