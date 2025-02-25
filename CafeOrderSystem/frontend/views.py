from django.shortcuts import render

def base(request):
    return render(request,'menu/base.html')
