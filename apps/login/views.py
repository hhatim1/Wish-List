from django.shortcuts import render, redirect
from .models import User
#from ..models import User
from django.contrib import messages
##################################
def index(request):
    return render(request, "login/index.html")

##################################
def register(request):
    result = User.objects.validate_and_register(request.POST)
    if result[0] == False:
        context = {
            'result':result[1]
        }
        return render(request, "login/index.html", context)
    if result[0] == True:
        context = {
            'name': result[1],
        }
        return render(request, "login/index.html", context)
###############################################################
def login(request):
    result = User.objects.validate_and_login(request.POST)
    if result[0] == False:
        context = {
            'result':result[1]
        }
        return render(request, "login/index.html", context)
    if result[0] == True:

        request.session['user_name'] = result[1][0].name
        request.session['user_id'] = result[1][0].id

        return redirect('wishlist:index')
    
