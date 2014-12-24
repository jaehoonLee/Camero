from django.conf.urls import patterns, include, url
from django.contrib import admin
from Main.views import *
from UserInfo.views import *

urlpatterns = patterns('',
    #web
    url(r'^$', main_page),
    url(r'^myinfo_page/', myinfo_page),
    url(r'^calculate_budget/', calculate_budget),
    url(r'^mystatus/(?P<order_num>\d+)/', mystatus, name='mystatus'),

    # user
    url(r'^customer_register_user/', customer_register_user),
    url(r'^translater_register_user/', translater_register_user),
    url(r'^login_user/', login_user),
    url(r'^logout_user/', logout_user),
    url(r'^register_order/', register_order),

    # url(r'^TranslateWeb/', include('TranslateWeb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
