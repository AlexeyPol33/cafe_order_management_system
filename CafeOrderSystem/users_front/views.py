import requests
from django.shortcuts import render
from .forms import RegistrationForm
from django.urls import reverse

def login_view(request):
    return render(
        request=request,
        template_name='login.html',
        context={},
        status=200)


def registration_view(request):
    form = None
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                'error/error.html', # TODO Добавить шаблон ошибки
                {'status':400,
                 'message': "Не верно заполнена форма"},
                 status=400)
    else:
        return render(
            request=request,
            template_name='registration.html',
            context={'form': RegistrationForm()})

    form_data = form.cleaned_data
    if form_data['password'] != form_data['password_repeat']:
        return render(
            request=request,
            template_name='registration.html',
            context={
                'form': RegistrationForm(),
                'error':'Пароли не совпадают'})
    
    # Запрос к внутреннему api: создание нового пользователя
    url = request.build_absolute_uri(reverse('users:users-list'))
    req_data = {
        'username':form_data['username'],
        'password':form_data['password'],
        'is_active': True}
    req = requests.post(url, json=req_data)
    if req.status_code != 201:
        return render(
            request,
            'error/error.html', # TODO Добавить шаблон ошибки
            {'status':req.status_code,
             'message': req.text},
            status=400)

    # Запрос к внутреннему api: выпуск токенов
    url = request.build_absolute_uri(reverse('users:token_obtain_pair'))
    req_data = {
        "username": form_data['username'],
        "password": form_data['password']}
    req = requests.post(url, json=req_data)
    if req.status_code != 200:
        return render(
            request,
            'error/error.html', # TODO Добавить шаблон ошибки
            {'status':req.status_code,
             'message': req.text},
            status=500)
    req = req.json()
    
    # Устанавливаем токены в cookies
    response = render(
        request,
        'welcome.html',
        {'username': form_data['username']})
    response.set_cookie(
        key='access_token',
        value=req['access'],
        httponly=True,
        secure=False, # TODO Поменять при переходе на https
        samesite="Lax",
        max_age=3600
    )
    response.set_cookie(
        key='refresh_token',
        value=req['refresh'],
        httponly=True,
        secure=False, # TODO Поменять при переходе на https
        samesite="Lax",
        max_age=7 * 24 * 3600
    )
    return response
