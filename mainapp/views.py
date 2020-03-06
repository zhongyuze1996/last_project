import json
import os
import uuid

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import re

from zyz_lastproject import settings
from utils.send_mess import YunPian
from utils.random_code import get_random

from mainapp.models import Banner

from redis import Redis
red=Redis(host='127.0.0.1',port=6379)
# Create your views here.
def show_host(request):
    banners=Banner.objects.filter(status=1)
    dict={'banners':banners}
    return render(request,'host.html',dict)


@csrf_exempt
def login_logic(request):
    mobile=request.POST.get('mobile')
    check=request.POST.get('check')
    code=red.get(mobile+'_2').decode()
    print(check,mobile,code)
    if check==code:
        return HttpResponse('yes')
    else:
        return HttpResponse('no')


def login_page(request):
    return render(request,'login.html')


@csrf_exempt
def get_code(request):
    mobile=request.POST.get('mobile')
    if red.get(mobile):
        return HttpResponse('0')
    if re.match(r"^1[35678]\d{9}$", mobile):
        code=get_random(5)
        print(code)
        red.setex(mobile,60,code)
        red.setex(mobile+'_2',300,code)
        yunpian = YunPian(settings.APIKEY)
        yunpian.send_message(mobile, code)
        return HttpResponse('1')
    else:
        return HttpResponse('0')

@csrf_exempt
def add_newbanner(request):
    try:
        title=request.POST.get('title')
        status=request.POST.get('status')
        img=request.FILES.get('pic')
        id=str(uuid.uuid4())
        extend=os.path.splitext(img.name)[1]
        print(title,status,img)
        img.name=id+extend
        Banner.objects.create(title=title,status=status,pic=img)

        return HttpResponse(1)
    except:
        return HttpResponse(0)

@csrf_exempt
def show_banners(request):
    banners=Banner.objects.all()
    def default(n):
        if isinstance(n,Banner):
            dict={'id':n.id,'title':n.title,'status':n.status,'pic':n.pic.name,"create_time":str(n.create_time)}
            return dict
    js=json.dumps(list(banners),default=default)
    return HttpResponse(js)



@csrf_exempt
def banner(request):
    oper=request.POST.get('oper')
    if oper == "edit":
        id = request.POST.get('id')
        title = request.POST.get('title')
        status = request.POST.get('status')
        print(id,status)
        banner = Banner.objects.get(id=id)
        banner.title=title
        banner.status=int(status)
        banner.save()
    elif oper == 'del':
        id = request.POST.get('id')
        Banner.objects.get(id=id).delete()
    return HttpResponse(1)