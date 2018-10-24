from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mainapp.models import MyUser, Source, Sort, Note ,Note_middle ,Team
from django.urls import reverse
import hashlib

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    user = request.user if request.user.is_authenticated else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'mainapp/index.html', content)

def about(request):
    user = request.user if request.user.is_authenticated else None
    content = {
        'active_menu': 'about',
        'user': user,
    }
    return render(request, 'mainapp/about.html', content)

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.save()
                new_my_user = MyUser(user=new_user, nickname=request.POST.get('nickname', ''))
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'signup',
        'state': state,
        'user': None,
    }
    return render(request, 'mainapp/signup.html', content)

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'login',
        'state': state,
        'user': None
    }
    return render(request, 'mainapp/login.html', content)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))

@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
                user = None
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'set_password',
        'state': state,
    }

    return render(request, 'mainapp/set_password.html', content)

@login_required
def add_note(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_book = Book(
                name=request.POST.get('name', ''),
                author=request.POST.get('author', ''),
                category=request.POST.get('category', ''),
                price=request.POST.get('price', 0),
                publish_date=request.POST.get('publish_date', '')
        )
        new_book.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_note',
        'state': state,
    }
    return render(request, 'mainapp/add_note.html', content)

@login_required
def add_note_auto(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_book = Book(
                name=request.POST.get('name', ''),
                author=request.POST.get('author', ''),
                category=request.POST.get('category', ''),
                price=request.POST.get('price', 0),
                publish_date=request.POST.get('publish_date', '')
        )
        new_book.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_note',
        'state': state,
    }
    return render(request, 'mainapp/add_note_auto.html', content)

@login_required
def add_note_manual(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_book = Book(
                name=request.POST.get('name', ''),
                author=request.POST.get('author', ''),
                category=request.POST.get('category', ''),
                price=request.POST.get('price', 0),
                publish_date=request.POST.get('publish_date', '')
        )
        new_book.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_note',
        'state': state,
    }
    return render(request, 'mainapp/add_note_manual.html', content)
