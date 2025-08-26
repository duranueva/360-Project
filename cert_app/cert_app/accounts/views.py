from django.shortcuts import render, HttpResponse
from .models import query_users

def home(request):
    users = query_users()
    """
    print(type(users))
    print("\n\n\n")
    print(users)
    print("\n\n\n")
    """
    return render(request,"home.html",{'users': users})

def home2(request):
    users = query_users()
    return render(request,"home2.html",{'users': users})