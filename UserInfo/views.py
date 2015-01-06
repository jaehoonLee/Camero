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
        id = request.POST['username']
        nickname = id.split("@")[0]

        #check nickname
        translater_size = len(Translater.objects.filter(nickname=nickname))
        index = 1
        while translater_size != 0:
            nickname = id.split("@")[0] + str(index)
            translater_size = len(Translater.objects.filter(nickname=nickname))

        Translater.objects.create_translator(nickname, 0, user)

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

def translater_active_request(request):
    username = request.POST['username']
    nickname = request.POST['nickname']
    phone = request.POST['phone1']
    phone2 = request.POST['phone2']
    phone3 = request.POST['phone3']
    service_availables = request.POST.getlist('service_available')
    language_availables = request.POST.getlist('language_available')
    translate_availables = request.POST.getlist('translate_available')

    school = request.POST['school1'] + '\n' + request.POST['school2']
    career = request.POST['career1'] + '\n' + request.POST['career2'] + '\n' + request.POST['career3']
    lang_experience = request.POST['lang_experience']

    print "username:" + username

    translater = request.user.translater
    translater.username = username
    translater.nickname = nickname
    translater.phone = phone
    translater.phone2 = phone2
    translater.phone3 = phone3


    service_available = ''
    for i in ['0', '1'] :
        if i in service_availables:
            service_available = service_available + '1' + ","
        else :
            service_available = service_available + '0' + ","
    service_available = service_available[:-1]

    language_available = ''
    for i in ['0', '1', '2', '3', '4', '5'] :
        if i in language_availables:
            language_available = language_available + '1' + ","
        else :
            language_available = language_available + '0' + ","
    language_available = language_available[:-1]

    translate_available = ''
    for i in ['0', '1', '2', '3', '4', '5', '6'] :
        if i in translate_availables:
            translate_available = translate_available + '1' + ","
        else :
            translate_available = translate_available + '0' + ","
    translate_available = translate_available[:-1]

    translater.service_available = service_available
    translater.language_available = language_available
    translater.translate_available = translate_available
    translater.school = school
    translater.career = career
    translater.lang_experience = lang_experience
    translater.active = 1
    translater.save()

    print username + ", " + nickname + ", " + phone + ", "
    print "service_available:" + str(service_available)
    print language_available
    print translate_available
    print school
    print career
    print lang_experience

    return redirect("main_page")

@csrf_exempt
def check_translater_nickname(request):
    nickname = request.POST['nickname']
    print nickname
    if request.user.translater.nickname == nickname :
        return HttpResponse(1)
    else :
        translaters = Translater.objects.filter(nickname=nickname)
        if len(translaters) == 0: # 아무도 없음
            return HttpResponse(1)
        else :
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