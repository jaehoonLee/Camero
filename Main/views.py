#-*- coding: utf-8 -*-
import simplejson, os
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from Camero.settings import UPLOAD_DIR
from docx import Document
from hwp5.hwp5txt import make
from Main.models import *

def main_page(request):
    if request.user.is_authenticated():
        try:
            orders = request.user.customer.order_set.all()
            #고객이라면
            return render_to_response('main_login.html', RequestContext(request, {'orders': orders}))
        except:
            try:
                #번역가라면
                pre_orders = []
                progress_orders = []
                complete_orders = []

                for order in request.user.translater.order_set.all():
                    if order.status == 3:
                        pre_orders.append(order)
                    elif order.status == 4 or order.status == 5:
                        progress_orders.append(order)
                    elif order.status == 6:
                        complete_orders.append(order)

                return render_to_response('main_login_translater.html', RequestContext(request, {'pre_orders': pre_orders, 'progress_orders' : progress_orders, 'complete_orders' : complete_orders}))
            except:
                return render_to_response('main_not_login.html', RequestContext(request))
    else :
        return render_to_response('main_not_login.html', RequestContext(request))


def myinfo_page(request):
    if request.user.is_anonymous():
        return render_to_response('main_not_login.html', RequestContext(request))
    else :
        return render_to_response('myinfo.html', RequestContext(request))

def makestatus(request):
    return render_to_response('status_1.html', RequestContext(request))

def mystatus(request, order_id):
    order = Order.objects.filter(id=order_id)
    #check user
    if order[0].customer.user.username != request.user.username:
        return HttpResponse("권한이 없습니다.")

    type = order[0].status
    if type == 1:
        return render_to_response('status_1.html', RequestContext(request))
    elif type == 2:
        return render_to_response('status_2.html', RequestContext(request, {'type': type, 'order': order[0], 'translaters':Translater.objects.all()}))
    elif type == 3:
        translaters = order[0].translaters.all()
        return render_to_response('status_2.html', RequestContext(request, {'type': type, 'order': order[0], 'translaters':translaters}))
    elif type == 4:
        return render_to_response('status_3.html', RequestContext(request, {'order': order[0]}))
    elif type == 5:
        return render_to_response('status_4.html', RequestContext(request, {'order': order[0]}))
    else:
        return render_to_response('status_5.html', RequestContext(request, {'order': order[0]}))

def translater_mystatus(request, order_id):
    order = Order.objects.filter(id=order_id)
    #check user
    translater = order[0].translaters.all()[0]
    if translater.user.username != request.user.username:
        return HttpResponse("권한이 없습니다.")

    return render_to_response('translate_detail.html', RequestContext(request, {'order': order[0]}))

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

        if int(status) == 2:
            size = int(request.POST['size'])
            for num in range(0, size):
                translater_id = request.POST[str(num)]
                translater = Translater.objects.filter(id=translater_id)[0]
                order.translaters.add(translater)

        elif int(status) == 3:
            sel_translater_id = int(request.POST['translater'])
            for translater in order.translaters.all():
                if translater.id == sel_translater_id:
                    continue
                else :
                    order.translaters.remove(translater)

        elif int(status) == 4: #번역자 입장
            print "HA"
            print int(status)
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
            return redirect("main_page", order_id=order_id)

        #elif int(status) == 5: #번역물 수령 완료

        order.status = int(order.status) + 1
        order.save()

    return redirect("mystatus", order_id=order_id)