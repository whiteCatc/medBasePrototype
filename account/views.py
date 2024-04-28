from django.shortcuts import render

# Create your views here.

def account(request):
    return render(request, "account/account.html")

def information(request):
    return render(request, "account/information.html")

def plans(request):
    return render(request, "account/plans.html")
