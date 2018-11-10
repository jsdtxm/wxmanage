from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mainapp.models import MyUser, Source, Sort, Note ,Team
from django.urls import reverse
from .note_form import Note_form
import hashlib
import base64

def index(request):
    user = request.user if request.user.is_authenticated else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'mainapp/index.html', content)

def abt(request):
    user = request.user if request.user.is_authenticated else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'mainapp/index_test.html', content)

def about(request):
    user = request.user if request.user.is_authenticated else None
    content = {
        'active_menu': 'about',
        'user': user,
    }
    return render(request, 'mainapp/about.html', content)

def pdf_viewer(request):
    user = request.user if request.user.is_authenticated else None
    content = {
        'user': user,
    }
    return render(request, 'mainapp/pdf_viewer.html', content)

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
        new_book = Note(
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
        new_book = Note(
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
    if request.method == 'POST':
        form = Note_form(request.POST,request.FILES)
        if form.is_valid():
            data = form.clean()
            new_note = Note(
                title = data['title'],
                authors = data['authors'],
                # source=data['source'],
                doi = data['doi'],
                institution = data['institution'],
                sore_year = data['sore_year'],
                abstract = data['abstract'],
                keywords = data['keywords'],
                upfile = data['upfile'],
                creater = request.user.myuser
            )
            team = Team.objects.get(pk=data['team_choice'])

            if len(Source.objects.filter(name=data['source']))!=0 :
                source = Source.objects.get(name=data['source'])
            else:
                source = Source(name=data['source'],source_type=data['source_select'])
                source.save()
            new_note.source = source

            new_note.save()
            team.notes_count += 1
            team.notes.add(new_note)
            team.save()
            # print(new_note)
            return HttpResponseRedirect(reverse('view_note_list'))
        else:
            print(form.errors)
    else :
        form = Note_form()

    return render(request, 'mainapp/add_note_manual.html', {'form':form})

@login_required
def view_note_list(request):
    user = request.user
    team = request.GET.get('team', 'all')

    myteam_list = Team.objects.filter(creater=user.myuser) | Team.objects.filter(managers=user.myuser) | Team.objects.filter(members=user.myuser)
    myteam_list = myteam_list.distinct()

    if team == 'all' or team == 'my' or Team.objects.filter(id=team).count() == 0:
        try:
            note_list = Team.objects.all()[0].notes.filter(show=True)
            team = Team.objects.all()[0].id
        except:
            note_list = []

    else:
        note_list = Team.objects.filter(id=team)[0].notes.filter(show=True)

    #搜索
    #检索改进到（标题、关键词、摘要）后期做正文
    if request.method == 'POST':
        keyword = request.POST.get('keywords', '')
        note_list = Note.objects.filter(title__contains=keyword)
        query_category = 'all'
    #分页
    paginator = Paginator(note_list, 10)
    page = request.GET.get('page')
    try:
        note_list = paginator.page(page)
    except PageNotAnInteger:
        note_list = paginator.page(1)
    except EmptyPage:
        note_list = paginator.page(paginator.num_pages)

    page_range = range(1,paginator.num_pages+1)

    content = {
        'user': user,
        'active_menu': 'view_note',
        'team_list': myteam_list,
        'note_list': note_list,
        'page_range':page_range,
        'team_id': team,
    }
    return render(request, 'mainapp/view_note_list.html', content)

@login_required
def user_center(request):
    user = request.user
    otype = request.GET.get('otype', '')
    team_list = Team.objects.all()
    myteam_list = []
    content = {
        'user': user,
        'ckuser':user,
    }

    if otype in ['','person']:
        for iteam in team_list:
            if user.myuser == iteam.creater or user.myuser in iteam.managers.all() or user.myuser in iteam.members.all():
                myteam_list.append(iteam)
        content['myteam_list'] = myteam_list
        return render(request, 'mainapp/user_person.html', content)
    elif otype == 'account':
        return render(request, 'mainapp/user_account.html', content)
    elif otype == 'passwd':
        return render(request, 'mainapp/user_passwd.html', content)
    elif otype == 'newteam':
        return render(request, 'mainapp/user_newteam.html', content)
    elif otype == 'team':
        myteam_list = Team.objects.filter(creater=user.myuser) | Team.objects.filter(managers=user.myuser) | Team.objects.filter(members=user.myuser)
        myteam_list = myteam_list.distinct()
        otherteam_list = Team.objects.exclude(creater=user.myuser).exclude(managers=user.myuser).exclude(members=user.myuser)
        print(myteam_list)
        print(otherteam_list)
        # for team in team_list:
            
        #     if user.myuser == team.creater or user.myuser in team.managers.all() or user.myuser in team.members.all():
        #         # print(user.myuser == team.creater)
        #         myteam_list.append(team)
        #     else:
        #         otherteam_list.append(team)
        
        content['otherteam_list'] = otherteam_list
        content['myteam_list'] = myteam_list

        return render(request, 'mainapp/user_team_list.html', content)

@login_required
def user_center_team(request):
    user = request.user
    team_id = request.GET.get('id', '')

    if team_id == '':
        return HttpResponseRedirect(reverse('view_note_list'))
    try:
        team = Team.objects.get(pk=team_id)
    except Note.DoesNotExist:
        return HttpResponseRedirect(reverse('view_note_list'))

    members = team.members.all()
    managers = team.managers.all()

    content = {
        'user': user,
        'team': team,
        'members':members,
        'managers':managers,
    }

    return render(request, 'mainapp/user_team.html', content)

@login_required
def user_center_user(request):
    user = request.user
    ckuser_id = request.GET.get('id', '')

    if ckuser_id == '':
        ckuser = user
    try:
        ckuser = User.objects.get(pk=ckuser_id)
    except Note.DoesNotExist:
        ckuser = user

    content = {
        'user': user,
        'ckuser': ckuser,
    }

    return render(request, 'mainapp/user_person.html', content)

@login_required
def detail(request):
    user = request.user
    note_id = request.GET.get('id', '')
    if note_id == '':
        return HttpResponseRedirect(reverse('view_note_list'))
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        return HttpResponseRedirect(reverse('view_note_list'))
        
    content = {
        'user': user,
        'active_menu': 'view_book',
        'note': note,
    }
    return render(request, 'mainapp/detail.html', content)

@login_required
def delnote(request):
    user = request.user
    note_id = request.GET.get('id', '')
    team_id = request.GET.get('team', '')
    if note_id == '' or team_id == '':
        return HttpResponseRedirect(reverse('view_note_list'))
    try:
        note = Note.objects.get(pk=note_id)
        team = Team.objects.get(pk=team_id)
        if user.myuser == team.creater or user.myuser in team.managers.all():
            # print("授权成功")
            # note.delete()
            note.show = False
            team.notes_count -=1 
            team.save()
            note.save()
        else :
            pass
            # print("授权失败")

    except Note.DoesNotExist:
        return HttpResponseRedirect(reverse('view_note_list'))

    return HttpResponseRedirect(reverse('view_note_list'))
