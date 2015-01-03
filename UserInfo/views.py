#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from UserInfo.models import *

#User Login
def customer_register_user(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST['username'],
                                    password=request.POST['password'],
                                    email=request.POST['username'])
        user.save()

        #make customer
        nickname = request.POST['username']
        nickname = nickname.split("@")[0]
        Customer.objects.create_customer(nickname, '', False, '', '', user)

    if user is not None:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

def translater_register_user(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST['username'],
                                    password=request.POST['password'],
                                    email=request.POST['username'])
        user.save()

        #make customer
        nickname = request.POST['username']
        nickname = nickname.split("@")[0]
        Translater.objects.create_translator(nickname, 0, 0, '', request.POST['username'], False, '', '', user)

    if user is not None:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

def update_translater(request):
    translater_id = request.POST['translater_id']
    translaters = Translater.objects.filter(id=translater_id)
    for translater in translaters :
        translater.active = True
        translater.save()
    return redirect("admin_page")

@csrf_exempt
def check_translater_nickname(request):
    nickname = request.POST['nickname']
    print nickname
    translaters = Translater.objects.filter(nickname=nickname)
    if len(translaters) == 0: # 아무도 없음
        return HttpResponse(1)
    else:
        return HttpResponse(0)


@csrf_exempt
def login_user(request):
    if request.method == 'POST' :
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.POST.has_key('remember') == False:
                    request.session.set_expiry(0)
            return HttpResponseRedirect('/')

        else:
            return render_to_response('../../Camero/templates/main_not_login.html', RequestContext(request))
    else:
        return render_to_response('../../Camero/templates/main_not_login.html', RequestContext(request))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')