# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class GeneralUser(models.Model):
    user = models.OneToOneField(User)
    kind = models.IntegerField(null=True)

class Product(models.Model):
    name = models.CharField(max_length=128)
    npc = models.CharField(max_length=20)
    stock = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    likes = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)

class UserLikeProduct(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)


class Ticket(models.Model):
    total = models.FloatField(null=True)
    date = models.DateTimeField(auto_now=True)
    buyer = models.ForeignKey(User)


class Sale(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(null=False, default=1)
    ticket = models.ForeignKey(Ticket)
    price = models.IntegerField(null=False)
