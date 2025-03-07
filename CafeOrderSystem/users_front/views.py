from django.shortcuts import render

def login_view(request):
    return render(
        request=request,
        template_name='login.html',
        context={},
        status=200)

def registration_view(request):
    return render(
        request=request,
        template_name='registration.html'
    )