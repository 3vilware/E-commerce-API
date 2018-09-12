from models import *
from django.http import HttpResponse
import json
import httplib
from httplib import responses as rp
#DELETE AFTER
from django.views.decorators.csrf import csrf_exempt
import jwt
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict



file = open("key.pem","r")
SERVER_KEY = file.read()
TOKEN_LIFE = 3600

@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')
        repeatPass = request.POST.get('repeat')
        kind = request.POST.get('kind')

        try:
            kind = int(kind)
        except ValueError:
            return HttpResponse(json.dumps({"Error":"Kind must be an integer value"}), content_type="application/json",
                                status=httplib.PRECONDITION_FAILED)

        if password == repeatPass:
            newUser = User()
            newUser.set_password(password)
            newUser.username = user
            newUser.save()
            newGeneral = GeneralUser(user=newUser, kind=kind)
            newUser.save()
        else:
            return HttpResponse(json.dumps({"Error": "Passwords does not match"}), content_type="application/json",
                                status=httplib.PRECONDITION_FAILED)

    else:
        return HttpResponse(json.dumps({"Error": "POST method is required"}), content_type="application/json",
                            status=httplib.BAD_REQUEST)

    return HttpResponse(json.dumps({"Success": "User created successfully"}), content_type="application/json",
                        status=httplib.CREATED)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('user')
        password = request.POST.get('password')

        user = authenticate(username=usuario, password=password)

        if user:
            try:
                queryUser = User.objects.get(username=usuario)
                if queryUser.check_password(password):
                    data = {"UserId": queryUser.pk, "exp": datetime.utcnow() + timedelta(seconds=TOKEN_LIFE)}
                    token = jwt.encode(data, SERVER_KEY, algorithm='HS256')

                    return HttpResponse(json.dumps({"token": token}), content_type="application/json",
                                        status=httplib.ACCEPTED)
                else:
                    return HttpResponse(json.dumps({"Error": "Bad user or password"}), content_type="application/json",
                                        status=httplib.UNAUTHORIZED)

            except ObjectDoesNotExist:
                return HttpResponse(json.dumps({"Error": "Bad user or password"}), content_type="application/json",
                                    status=httplib.UNAUTHORIZED)


    return HttpResponse(json.dumps({"Error": "Bad user or password"}), content_type="application/json", status=httplib.UNAUTHORIZED)


@csrf_exempt
def createProduct(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        npc = request.POST.get('npc')
        stock = request.POST.get('stock')
        price = request.POST.get('price')

        info = request.META['HTTP_AUTHORIZATION']
        try:
            data = jwt.decode(info, SERVER_KEY, algorithms=['HS256'])
            print "Datos: ", data
        except jwt.ExpiredSignature:
            return HttpResponse(json.dumps({"Error": "Expired token"}), content_type="application/json",
                                status=httplib.UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return HttpResponse(json.dumps({"Error": "Invalid token"}), content_type="application/json",
                                status=httplib.UNAUTHORIZED)


        newProduct = Product(name=name, npc=npc, stock=int(stock), price=int(price))
        try:
            newProduct.save()
            return HttpResponse(json.dumps({"Success": "A new product has been created!"}), content_type="application/json",
                                status=httplib.CREATED)
        except ValueError:
            return HttpResponse(json.dumps({"Error": "Bad information"}), content_type="application/json",
                                status=httplib.PRECONDITION_FAILED)
    else:
        return HttpResponse(json.dumps({"Error": "Post method is required"}), content_type="application/json",
                            status=httplib.BAD_REQUEST)


def getProduct(request, id):
    id = int(id)
    info = request.META['HTTP_AUTHORIZATION']

    try:
        data = jwt.decode(info, SERVER_KEY, algorithms=['HS256'])
        print "Datos: ", data
    except jwt.ExpiredSignature:
        return HttpResponse(json.dumps({"Error": "Expired token"}), content_type="application/json",
                            status=httplib.UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return HttpResponse(json.dumps({"Error": "Invalid token"}), content_type="application/json",
                            status=httplib.UNAUTHORIZED)

    try:
        product = Product.objects.get(pk=id)
        data = {"ID":product.pk, "Name":product.name, "NPC":product.npc, "Stock":str(product.stock),
                "Price": str(product.price), "likes": product.likes ,"last_update": str(product.last_update)}
        dataJson = json.dumps(data)

        return HttpResponse(dataJson, content_type="application/json",
                            status=httplib.OK)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"Error": "Product does not exists"}), content_type="application/json",
                            status=httplib.NOT_FOUND)

@csrf_exempt
def updateProductPrice(request):
    if request.method == 'POST':
        # body = QueryDict(request.body)
        # print body.getlist('id')
        # id = request.GET.get('id')
        # body = json.dumps(request.body)

        newPrice = request.POST.get('price')
        id = request.POST.get('id')
        id = int(id)

        info = request.META['HTTP_AUTHORIZATION']
        try:
            data = jwt.decode(info, SERVER_KEY, algorithms=['HS256'])
            print "Datos: ", data
        except jwt.ExpiredSignature:
            return HttpResponse(json.dumps({"Error": "Expired token"}), content_type="application/json",
                                status=httplib.UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return HttpResponse(json.dumps({"Error": "Invalid token"}), content_type="application/json",
                                status=httplib.UNAUTHORIZED)

        try:
            product = Product.objects.get(pk=id)
            product.price = int(newPrice)
            product.last_update = datetime.utcnow()
            product.save()

            return HttpResponse(json.dumps({"Success": "Product has been updated!"}), content_type="application/json",
                                status=httplib.OK)
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({"Error": "Product does not exist"}), content_type="application/json",
                                status=httplib.NOT_FOUND)

    else:
        return HttpResponse(json.dumps({"Error": "POST method is required"}), content_type="application/json",
                            status=httplib.BAD_REQUEST)


@csrf_exempt
def deleteProduct(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        id = int(id)

        info = request.META['HTTP_AUTHORIZATION']
        try:
            data = jwt.decode(info, SERVER_KEY, algorithms=['HS256'])
            print "Datos: ", data
        except jwt.ExpiredSignature:
            return HttpResponse(json.dumps({"Error": "Expired token"}), content_type="application/json",
                                status=httplib.UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return HttpResponse(json.dumps({"Error": "Invalid token"}), content_type="application/json",
                                status=httplib.UNAUTHORIZED)

        try:
            product = Product.objects.get(pk=id)
            product.delete()

            return HttpResponse(json.dumps({"Success": "Product has been deleted!"}),
                                content_type="application/json",
                                status=httplib.OK)
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({"Error": "Product does not exist"}), content_type="application/json",
                                status=httplib.NOT_FOUND)

    else:
        return HttpResponse(json.dumps({"Error": "POST method is required"}), content_type="application/json",
                            status=httplib.BAD_REQUEST)


