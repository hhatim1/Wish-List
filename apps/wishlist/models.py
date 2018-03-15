# Create your models here.
from __future__ import unicode_literals
from django.db.models import Count
from django.db import models
from ..login.models import User
######################################################

class ProductManager(models.Manager):
    def addProduct(self, postData, user_id):
        errors = []
        response = {}
        if len("".join(postData['productName'].split())) < 3:
            errors.append("Please give your product a name at least 3 characters long.")
            response['status']=False
            response['errors']=errors
        else:
            response['status']=True
            user = User.objects.get(id=user_id)
            newProduct=Wishlist.objects.create(name=postData['productName'], created_by=user)
            newProduct.wished_by.add(user)
            newProduct.save()
            response['product']=newProduct
        return response

##########################################################
class Wishlist(models.Model):
    name = models.CharField(max_length=255)
    created_by=models.ForeignKey(User,related_name='created_prodcut',null=True)
    wished_by=models.ManyToManyField(User,related_name='wished_prodcut',null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = ProductManager()
