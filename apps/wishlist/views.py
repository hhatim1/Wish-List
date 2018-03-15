
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from ..login.models import User
from .models import *
from django.core.urlresolvers import reverse
#from django.db.models import Count
######################################
def index(request):
    if not 'user_name' in request.session:
        messages.add_message(request, messages.INFO, "Please Login")
        return redirect('login:index')
        #return render(request, "wishlist:index.html", context)
    me = User.objects.get(id = request.session['user_id'])
    context = {
        'me' : me,
        'my_items' : Wishlist.objects.filter(wished_by=me),
        'other_items' : Wishlist.objects.exclude(wished_by=me)
    }
    return render(request, "wishlist/index.html", context)

def logout(request):
    request.session.flush()
    return redirect('login:index')

#def Dashboard(request):


def create_item(request):
    result = Wishlist.objects.addProduct(request.POST, request.session['user_id'])
    if result['status']:
        return redirect('wishlist:index')
    return redirect('/')

def wishlist(request):
    if request.method == 'POST':
        add.objects.my_list(request.POST)
        return redirect('wishlist:index')

def leave(request, item_id):
    user = User.objects.get(id=request.session['user_id'])
    item = Wishlist.objects.get(id=item_id)
    item.wished_by.remove(user)
    item.save()
    return redirect('/wishlist/')


def join(request, item_id):
    user = User.objects.get(id=request.session['user_id'])
    item = Wishlist.objects.get(id=item_id)
    item.wished_by.add(user)
    item.save()
    return redirect('/wishlist/')

def info(request, item_id):
    context = {
    'item' : Wishlist.objects.get(id=item_id)
    }
    return render(request, 'wishlist/info.html', context)
