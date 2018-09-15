from models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import json
import httplib
import jwt
from django.http import JsonResponse


def getKey():
    file = open("key.pem","r")
    key = file.read()

    return key


def isLiked(user, product):
    try:
        up = UserLikeProduct.objects.get(product=product, user=user)
    except ObjectDoesNotExist:
        up = False

    if up:
        return True
    else:
        return False


def checkToken(request):
    info = request.META['HTTP_AUTHORIZATION']
    SERVER_KEY = getKey()

    try:
        data = jwt.decode(info, SERVER_KEY, algorithms=['HS256'])
        userId = data["userId"]
        user = User.objects.get(pk=userId)
        return user
    except jwt.ExpiredSignature:
        return HttpResponse(json.dumps({"error": "Expired token"}), content_type="application/json",
                            status=httplib.UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return HttpResponse(json.dumps({"error": "Invalid token"}), content_type="application/json",
                            status=httplib.UNAUTHORIZED)


