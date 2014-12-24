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

            return render_to_response('main_login.html', RequestContext(request, {'orders': orders}))
        except:
            try:
                request.user.translater.order_set.all()
                return render_to_response('main_not_login.html', RequestContext(request))
            except:
                return render_to_response('main_not_login.html', RequestContext(request))
    else :
        return render_to_response('main_not_login.html', RequestContext(request))


def myinfo_page(request):
    if request.user.is_anonymous():
        return render_to_response('main_not_login.html', RequestContext(request))
    else :
        return render_to_response('myinfo.html', RequestContext(request))

def mystatus(request, order_num):
    print order_num
    type = int(order_num)
    if type == 1:
        return render_to_response('status_1.html', RequestContext(request))
    elif type == 2 or type == 3:
        return render_to_response('status_2.html', RequestContext(request, {'type': type}))
    elif type == 4:
        return render_to_response('status_3.html', RequestContext(request))
    elif type == 5:
        return render_to_response('status_4.html', RequestContext(request))
    else:
        return render_to_response('status_5.html', RequestContext(request))

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
        print "H"
        #Save Files
        if 'file' in request.FILES:
            print "H1"
            file = request.FILES['file']
            filename = file._name
            user = request.user

            fp = open(('%s/Files/%s_%s' % (UPLOAD_DIR, user.username, filename)), 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()

    #Save Order
    Order.objects.create_order(type, 2, request.user.customer, originalLang, changeLang, 0, filename)

    return redirect("mystatus", order_num='2')