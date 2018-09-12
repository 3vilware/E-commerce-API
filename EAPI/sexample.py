from models import *
from django.http import HttpResponse
import json
import httplib
from httplib import responses as rp
#DELETE AFTER
from django.views.decorators.csrf import csrf_exempt
import jwt
from datetime import datetime, timedelta

"""
pyjwt
"""
file = open("key.pem","r")

SERVER_KEY = file.read()


@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')

        data = {"User": user, "exp": datetime.utcnow() + timedelta(seconds=60) }
        token = jwt.encode(data, SERVER_KEY, algorithm='HS256')
        print "Ahora: ", datetime.utcnow()
        print "Despues ", datetime.utcnow() + timedelta(seconds=10)

        return HttpResponse(json.dumps({"token": token}), content_type="application/json", status=httplib.ACCEPTED)

    return HttpResponse(json.dumps({"Error": "Bad credentials"}), content_type="application/json", status=httplib.UNAUTHORIZED)


def getTest(request):
    obj = Test.objects.all()
    lista = []

    print "Autorizacion: ", request.META['HTTP_AUTHORIZATION']
    info = request.META['HTTP_AUTHORIZATION']

    try:
        data = jwt.decode(info, SERVER_KEY, algorithms=['HS256'])
        print "Datos: ", data
    except jwt.ExpiredSignature:
        return HttpResponse(json.dumps({"Error":"Expired signature"}), content_type="application/json", status=httplib.UNAUTHORIZED)

    for o in obj:
        data = {"Name": o.name}
        lista.append(data)

    return HttpResponse(json.dumps(lista), content_type="application/json", status=httplib.OK)


@csrf_exempt
def addTest(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        newTest = Test(name=name)
        newTest.save()
        print "CODE ", SERVER_KEY
        return HttpResponse(json.dumps({"OK":"CREADO"}), content_type="application/json", status=httplib.CREATED)

    return HttpResponse(json.dumps({"ERROR":"BAD"}), content_type="application/json", status=httplib.BAD_REQUEST)