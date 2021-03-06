#-*- coding: utf-8 -*-

import simplejson, os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from Camero.settings import UPLOAD_DIR
from docx import Document
from hwp5.hwp5txt import make
from Main.models import *
from django.core.mail import send_mail

def main_page(request):
    print "main_page"
    if request.user.is_authenticated():
        try:
            orders = request.user.customer.order_set.all()
            #고객이라면
            pre_orders = []
            progress_orders = []
            complete_orders = []

            for order in request.user.customer.order_set.all():
                print order.status
                if order.status == 2 or order.status == 3:
                    pre_orders.append(order)
                elif order.status == 4 or order.status == 5 or order.status == 6:
                    progress_orders.append(order)
                else:
                    complete_orders.append(order)

            return render_to_response('main_login.html', RequestContext(request, {'pre_orders': pre_orders, 'progress_orders' : progress_orders, 'complete_orders': complete_orders}))
        except:
            try:
                print "translater"
                #번역가라면
                pre_orders = []
                progress_orders = []
                complete_orders = []

                for order in request.user.translater.order_set.all():
                    if order.status == 2 or order.status == 3:
                        pre_orders.append(order)
                    elif order.status == 4 or order.status == 5 or order.status == 6:
                        progress_orders.append(order)
                    else:
                        complete_orders.append(order)

                service_available = request.user.translater.service_available.split(',')
                language_available = request.user.translater.language_available.split(',')
                translate_available = request.user.translater.translate_available.split(',')

                if request.user.translater.active == 0:
                    service_available = ['0', '0']
                    language_available = ['0', '0', '0', '0', '0', '0']
                    translate_available = ['0', '0', '0', '0', '0', '0', '0']


                print service_available

                translate = int(service_available[0])
                revision = int(service_available[1])

                lang1 = int(language_available[0])
                lang2 = int(language_available[1])
                lang3 = int(language_available[2])
                lang4 = int(language_available[3])
                lang5 = int(language_available[4])
                lang6 = int(language_available[5])

                field1 = int(translate_available[0])
                field2 = int(translate_available[1])
                field3 = int(translate_available[2])
                field4 = int(translate_available[3])
                field5 = int(translate_available[4])
                field6 = int(translate_available[5])
                field7 = int(translate_available[6])

                schools = request.user.translater.school.split('\n')
                careers = request.user.translater.career.split('\n')

                if request.user.translater.active == 0:
                    schools=['', '']
                    careers=['', '', '']


                return render_to_response('main_login_translater.html', RequestContext(request, {'translate': translate, 'revision': revision,
                                                                                                 'lang1': lang1, 'lang2': lang2, 'lang3': lang3, 'lang4': lang4, 'lang5': lang5, 'lang6': lang6,
                                                                                                 'field1': field1, 'field2': field2, 'field3': field3, 'field4': field4, 'field5': field5, 'field6': field6, 'field7': field7,
                                                                                                 'schools': schools, 'careers': careers,
                                                                                                 'active': request.user.translater.active,
                                                                                                 'pre_orders': pre_orders, 'progress_orders' : progress_orders, 'complete_orders' : complete_orders}))
            except:
                return render_to_response('main_not_login.html', RequestContext(request))
    else :
        return render_to_response('main_not_login.html', RequestContext(request))

def budget_admin_page(request):
    orders = Order.objects.filter(status=5)
    translaters = Translater.objects.filter(active=1)

    translaters_size = len(Translater.objects.all())
    customers_size = len(Customer.objects.all())

    return render_to_response('budget_admin.html', RequestContext(request, {'translaters_size': translaters_size, 'customers_size' : customers_size, 'orders': orders, 'translaters': translaters}))

def myinfo_page(request):
    if request.user.is_anonymous():
        return render_to_response('main_not_login.html', RequestContext(request))
    else :
        return render_to_response('myinfo.html', RequestContext(request))

def makestatus(request):
    pre_orders = []
    progress_orders = []
    complete_orders = []

    #대부분 고객이기 때문에
    for order in request.user.customer.order_set.all():
        print order.status
        if order.status == 2 or order.status == 3:
            pre_orders.append(order)
        elif order.status == 4 or order.status == 5 or order.status == 6:
            progress_orders.append(order)
        else:
            complete_orders.append(order)

    return render_to_response('status_1.html', RequestContext(request, {'pre_orders': pre_orders, 'progress_orders' : progress_orders, 'complete_orders': complete_orders}))

def mystatus(request, order_id):
    order = Order.objects.filter(id=order_id)[0]
    #check user
    if order.customer.user.username != request.user.username:
        return HttpResponse("권한이 없습니다.")

    pre_orders = []
    progress_orders = []
    complete_orders = []

    #대부분 고객이기 때문에
    for my_order in request.user.customer.order_set.all():
        if order.status == 2 or order.status == 3:
                    pre_orders.append(order)
        elif order.status == 4 or order.status == 5 or order.status == 6:
            progress_orders.append(my_order)
        elif my_order.status == 6:
            complete_orders.append(my_order)

    type = order.status
    if type == 1:#견적확인
        return render_to_response('status_1.html', RequestContext(request))
    elif type == 2:#번역가문의
        return render_to_response('status_2.html', RequestContext(request, {'type': type, 'order': order, 'translaters':Translater.objects.all(), 'pre_orders': pre_orders, 'progress_orders' : progress_orders, 'complete_orders': complete_orders}))
    elif type == 3:#번역가선정
        translaters = order.translaters.all()
        return render_to_response('status_3.html', RequestContext(request, {'type': type, 'order': order, 'translaters':translaters, 'pre_orders': pre_orders, 'progress_orders' : progress_orders, 'complete_orders': complete_orders}))
    elif type == 4:#결제
        return render_to_response('status_4.html', RequestContext(request, {'status' : 4, 'order': order, 'pre_orders': pre_orders, 'progress_orders' : progress_orders, 'complete_orders': complete_orders}))
    elif type == 5:#결제 확인
        return render_to_response('status_4.html', RequestContext(request, {'status' : 5, 'order': order, 'pre_orders': pre_orders, 'progress_orders' : progress_orders, 'complete_orders': complete_orders}))
    elif type == 6:#번역물 수령
        messages = order.message_set.all()
        return render_to_response('status_5.html', RequestContext(request, {'order': order, 'pre_orders': pre_orders, 'progress_orders': progress_orders, 'complete_orders': complete_orders, 'message_set': messages}))
    else:
        return redirect("main_page")

def translater_mystatus(request, order_id):
    order = Order.objects.filter(id=order_id)[0]

    #check user
    translater = order.translaters.all()[0]
    if translater.user.username != request.user.username:
        return HttpResponse("권한이 없습니다.")

    messages = order.message_set.all()
    return render_to_response('translate_detail.html', RequestContext(request, {'order': order, 'message_set': messages }))

@csrf_exempt
def calculate_budget(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            filename = file._name
            #print vars(file)

            #save file
            fp = open(('%s/%s' % (UPLOAD_DIR, file._name)), 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()

            fp = open(('%s/%s' % (UPLOAD_DIR, file._name)), 'r')
            size = 0

            #extension check
            name = filename.split(".")[0]
            extension = filename.split(".")[-1]
            if extension == 'txt':
                print "txt format"
                for line in fp:
                    size += len(line)
            elif extension == 'docx' or extension == 'doc':
                print "docx format"
                document = Document(fp)
                paragraphs = document.paragraphs
                for paragraph in paragraphs:
                    size += len(paragraph.text)
            elif extension == 'hwp':
                print "hwp format"
                args = {'<hwp5file>': file._name}
                make(args)
                fp2 = open(('%s/%s' % (UPLOAD_DIR, name + ".txt")), 'r')
                for line in fp2:
                    size += len(line)
                fp2.close()
                os.remove('%s/%s' % (UPLOAD_DIR, name + ".txt"))


            fp.close()

            #delete file
            os.remove('%s/%s' % (UPLOAD_DIR, file._name))

            len_translater = len(Translater.objects.all())
            result = {'budget': str(size * 10) + '원', 'transcount':  str(len_translater) + '명 대기 중'}

            return HttpResponse(simplejson.dumps(result), 'application/json')
        else :
            print 'HELLO'
    return HttpResponse(100)

def register_order(request):
    type = request.POST['type']
    originalLang = request.POST['originalLang']
    changeLang = request.POST['changeLang']
    filename =''
    if request.method == 'POST':
        #Save Files
        if 'file' in request.FILES:
            file = request.FILES['file']
            filename = file._name
            user = request.user

            fp = open(('%s/Files/%s_%s' % (UPLOAD_DIR, user.username, filename)), 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()

    #Save Order
    order = Order.objects.create_order(type, 2, request.user.customer, originalLang, changeLang, 0, filename)

    return redirect("mystatus", order_id=order.id)


def update_order(request, status):
    if request.method == 'POST':
        order_id = int(request.POST['order_id'])
        order = Order.objects.filter(id=order_id)[0]

        print int(status)

        #check user
        if order.customer.user.username != request.user.username:
            return HttpResponse("권한이 없습니다.")

        if int(status) == 2:#번역자 문의
            size = int(request.POST['size'])
            for num in range(0, size):
                translater_id = request.POST[str(num)]
                translater = Translater.objects.filter(id=translater_id)[0]
                order.translaters.add(translater)

        elif int(status) == 3:#번역자 선정
            sel_translater_id = int(request.POST['translater'])
            for translater in order.translaters.all():
                if translater.id == sel_translater_id:
                    continue
                else :
                    order.translaters.remove(translater)

        elif int(status) == 4: #결제확인 요청
            print "Check"
            #메일 알림 보내기
            '''
            file = request.FILES['file']
            filename = file._name
            user = request.user
            fp = open(('%s/CompleteFiles/complete_%s_%s' % (UPLOAD_DIR, user.username, filename)), 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()

            order.trans_filename = filename
            order.status = int(order.status) + 1
            order.save()
            return redirect("main_page")
            '''

        elif int(status) == 5: # 결제 확인
            print "Check3"
        elif int(status) == 6: # 수령 확인
            print "Check4"


        order.status = int(order.status) + 1
        order.save()

    return redirect("mystatus", order_id=order_id)


def make_order_message(request):
    if request.method == 'POST':
        type = int(request.POST['type']) #sender_type : 0=>고객, 1=>번역자
        order_id = request.POST['order_id']
        order = Order.objects.filter(id=order_id)[0]
        content = request.POST['content']

        message_len = len(order.message_set.all());

        if type == 0:
            sender = order.customer.nickname
            receiver = order.translaters.all()[0].nickname
            Message.objects.create_order(type, order, sender, receiver, content)

            return HttpResponseRedirect("/mystatus/" + order_id +"/#" + str(message_len))
        elif type == 1:
            sender = order.translaters.all()[0].nickname
            receiver = order.customer.nickname
            Message.objects.create_order(type, order, sender, receiver, content)

            return HttpResponseRedirect("/translater_mystatus/" + order_id +"/#" + str(message_len))


