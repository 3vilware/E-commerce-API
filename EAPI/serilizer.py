from models import *
from django.http import HttpResponse
import httplib
from django.views.decorators.csrf import csrf_exempt
import jwt
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
import commons as cm
from django.http import JsonResponse
from enumerations import UserKind
import json


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
            return JsonResponse({"error":"Kind must be an integer value"}, content_type="application/json",
                                status=httplib.PRECONDITION_FAILED)

        if password == repeatPass:
            newUser = User()
            newUser.set_password(password)
            newUser.username = user
            newUser.save()
            newGeneral = GeneralUser(user=newUser, kind=kind)
            newUser.save()
            newGeneral.save()
        else:
            return JsonResponse({"error": "Passwords does not match"}, content_type="application/json",
                                status=httplib.PRECONDITION_FAILED)

    else:
        return JsonResponse({"error": "POST method is required"}, content_type="application/json",
                            status=httplib.BAD_REQUEST)

    return JsonResponse({"success": "User created successfully"}, content_type="application/json",
                        status=httplib.CREATED)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('user')
        password = request.POST.get('password')
        SERVER_KEY = cm.getKey()

        user = authenticate(username=usuario, password=password)

        if user:
            try:
                queryUser = User.objects.get(username=usuario)
                if queryUser.check_password(password):
                    data = {"userId": queryUser.pk, "exp": datetime.utcnow() + timedelta(seconds=TOKEN_LIFE)}
                    token = jwt.encode(data, SERVER_KEY, algorithm='HS256')

                    return JsonResponse({"token": token}, content_type="application/json",
                                        status=httplib.ACCEPTED)
                else:
                    return JsonResponse({"error": "Bad user or password"}, content_type="application/json",
                                        status=httplib.UNAUTHORIZED)

            except ObjectDoesNotExist:
                return JsonResponse({"error": "Bad user or password"}, content_type="application/json",
                                    status=httplib.UNAUTHORIZED)


    return JsonResponse({"error": "Bad user or password"}, content_type="application/json", status=httplib.UNAUTHORIZED)



@csrf_exempt
def createProduct(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        npc = request.POST.get('npc')
        stock = request.POST.get('stock')
        price = request.POST.get('price')

        user = cm.checkToken(request)
        if not isinstance(user, User):
            return user

        permission = GeneralUser.objects.get(user=user)
        if permission.kind is UserKind.admin.value:
            newProduct = Product(name=name, npc=npc, stock=int(stock), price=int(price))
            try:
                newProduct.save()
                return JsonResponse({"success": "A new product has been created!"}, content_type="application/json",
                                    status=httplib.CREATED)
            except ValueError:
                return JsonResponse({"error": "Bad information"}, content_type="application/json",
                                    status=httplib.PRECONDITION_FAILED)
        else:
            return JsonResponse({"error":"Forbidden"}, content_type="application/json", status=httplib.FORBIDDEN)
    else:
        return JsonResponse({"error": "Post method is required"}, content_type="application/json",
                            status=httplib.BAD_REQUEST)


def getProduct(request, id):
    id = int(id)

    try:
        product = Product.objects.get(pk=id)
        data = {"id":product.pk, "Name":product.name, "NPC":product.npc, "Stock":str(product.stock),
                "Price": str(product.price), "likes": product.likes ,"last_update": str(product.last_update)}

        return JsonResponse(data, content_type="application/json",
                            status=httplib.OK, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Product does not exists"}, content_type="application/json",
                            status=httplib.NOT_FOUND)

@csrf_exempt
def updateProductPrice(request):
    if request.method == 'POST':
        newPrice = request.POST.get('price')
        id = request.POST.get('id')
        id = int(id)

        user = cm.checkToken(request)
        if not isinstance(user, User):
            return user

        permission = GeneralUser.objects.get(user=user)
        if permission.kind is UserKind.admin.value:

            try:
                product = Product.objects.get(pk=id)
                product.price = int(newPrice)
                product.last_update = datetime.utcnow()
                product.save()

                return JsonResponse({"success": "Product has been updated!"}, content_type="application/json",
                                    status=httplib.OK)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Product does not exist"}, content_type="application/json",
                                    status=httplib.NOT_FOUND)
        else:
            return JsonResponse({"error":"Forbidden"}, content_type="application/json", status=httplib.FORBIDDEN)

    else:
        return JsonResponse({"error": "POST method is required"}, content_type="application/json",
                            status=httplib.BAD_REQUEST)


@csrf_exempt
def deleteProduct(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        id = int(id)

        user = cm.checkToken(request)
        if not isinstance(user, User):
            return user

        permission = GeneralUser.objects.get(user=user)
        if permission.kind is UserKind.admin.value:
            try:
                product = Product.objects.get(pk=id)
                # product.delete()
                product.active = False
                product.save()

                return JsonResponse({"success": "Product has been deleted!"},
                                    content_type="application/json",
                                    status=httplib.OK)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Product does not exist"}, content_type="application/json",
                                    status=httplib.NOT_FOUND)
        else:
            return JsonResponse({"error":"Forbidden"}, content_type="application/json", status=httplib.FORBIDDEN)

    else:
        return JsonResponse({"error": "POST method is required"}, content_type="application/json",
                            status=httplib.BAD_REQUEST)



def getAllProducts(request, orderby):
    productList = []

    try:
        if str(orderby) == 'name':
            products = Product.objects.filter(active=True).order_by('name')
        else:
            products = Product.objects.filter(active=True).order_by('-likes')

        for product in products:
            data = {"id":str(product.pk), "Name":product.name, "NPC":product.npc, "Stock":str(product.stock),
                    "Price": str(product.price), "likes": product.likes ,"last_update": str(product.last_update)}
            productList.append(data)

        return JsonResponse(productList, content_type="application/json",
                            status=httplib.OK, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Product does not exists"}, content_type="application/json",
                            status=httplib.NOT_FOUND, safe=False)



def getProductByName(request, name):
    productList = []
    dataJson = {}

    try:
        products = Product.objects.filter(name__contains=name, active=True)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Product does not exists"}, content_type="application/json",
                            status=httplib.NOT_FOUND)

    if products:
        for product in products:
            data = {"id": str(product.pk), "Name": product.name, "NPC": product.npc, "Stock": str(product.stock),
                    "Price": str(product.price), "likes": product.likes, "last_update": str(product.last_update)}
            productList.append(data)

        return JsonResponse(productList, content_type="application/json",
                            status=httplib.OK, safe=False)
    else:
        return JsonResponse({"error": "No results found"}, content_type="application/json",
                            status=httplib.NO_CONTENT)


@csrf_exempt
def likeProduct(request):
    if request.method == 'POST':
        productId = request.POST.get('productId')

        user = cm.checkToken(request)
        if not isinstance(user, User):
            return user

        permission = GeneralUser.objects.get(user=user)
        if permission.kind is UserKind.registered.value:

            if cm.isLiked(user, productId):
                return JsonResponse({"warning": "That product already likes you"}, content_type="application/json",
                                    status=httplib.NOT_ACCEPTABLE)
            else:
                try:
                    product = Product.objects.get(pk=productId)
                except ObjectDoesNotExist:
                    return JsonResponse({"error": "Product does not exists"}, content_type="application/json",
                                        status=httplib.NOT_FOUND)

                product.likes = int(product.likes) + 1
                product.save()

                queryUser = User.objects.get(pk=user.pk)
                up = UserLikeProduct(user=queryUser, product=product)
                up.save()
                return JsonResponse({"success": "Like Saved!"}, content_type="application/json",
                                    status=httplib.OK)
        else:
            return JsonResponse({"error":"Forbidden"}, content_type="application/json", status=httplib.FORBIDDEN)



@csrf_exempt
def buyProduct(request):
    if request.method == 'POST':
        productId = request.POST.get('productId')
        quantity = int(request.POST.get('quantity'))

        user = cm.checkToken(request)
        if not isinstance(user, User):
            return user

        permission = GeneralUser.objects.get(user=user)
        if permission.kind is UserKind.registered.value:
            try:
                product = Product.objects.get(pk=productId)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Product does not exist"}, content_type="application/json",
                                    status=httplib.NO_CONTENT)

            if product.stock >= quantity:
                total = product.price * quantity

                newTicket = Ticket(total=total, buyer=user)
                newTicket.save()

                newSale = Sale(product=product, ticket=newTicket, price=product.price, quantity=quantity)
                product.stock = product.stock - quantity
                product.save()
                newSale.save()

                return JsonResponse({"success": "Purchase made successfully"}, content_type="application/json",
                                    status=httplib.OK)
            else:
                return JsonResponse({"error": "Insufficient stock"}, content_type="application/json",
                                    status=httplib.NOT_ACCEPTABLE)
        else:
            return JsonResponse({"error":"Forbidden"}, content_type="application/json", status=httplib.FORBIDDEN)



def salesLog(request):
    salesList =[]

    user = cm.checkToken(request)
    if not isinstance(user, User):
        return user

    permission = GeneralUser.objects.get(user=user)
    if permission.kind is UserKind.admin.value:
        tickets = Ticket.objects.all()

        if tickets:
            for ticket in tickets:
                sale = Sale.objects.get(ticket=ticket)
                data = {"id":ticket.pk, "date":str(ticket.date), "total":str(ticket.total), "product":sale.product.name,
                        "quantity":sale.quantity, "price":str(sale.price), "buyer":ticket.buyer.username}
                salesList.append(data)

            return JsonResponse(salesList, content_type="application/json", status=httplib.OK, safe=False)
        else:
            return JsonResponse({"error":"No data"}, content_type="application/json", status=httplib.NO_CONTENT, safe=False)

    else:
        return JsonResponse({"error": "Forbidden"}, content_type="application/json", status=httplib.FORBIDDEN)








