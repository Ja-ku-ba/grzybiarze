from django.shortcuts import render, redirect
from .models import Fung, Post, Like, Dislike
from .forms import User_form, Post_form
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'fungus/home.html', context)

def atlas(request):
    funguses = Fung.objects.all()
    context = {'funguses':funguses}
    return render(request, 'fungus/atlas.html', context)

def munschrom_page(request, pk):
    munschrom = Fung.objects.get(name=pk)
    context = {'munschrom':munschrom}
    return render(request, 'fungus/munschrom_page.html', context)

def register(request):
    form = User_form()
    status = 'r'
    context = {'form':form, 'status':status}
    if request.method == 'POST':
        form = User_form(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        messages.error(request, f'Hasła nie są identyczne {username} {email}')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nazwa użytkownika zajęta')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Już istnieje konto z podanym adresem email')
        if password1 != password2:
            messages.error(request, f'Hasła nie są identyczne {username} {email}')
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'No chyba nie') 
         
    return render(request, 'fungus/login_register.html', context)

def user_login(request):
    status = 'l'
    context = {'status':status}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
        except:
            messages.error(request, 'Login lub hasło jest niepoprawne')
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'klapa')
    return render(request, 'fungus/login_register.html', context)

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def add_post(request):
    form = Post_form()
    context = {'form':form}
    if request.method == 'POST':
        Post.objects.create(
            owner = request.user,
            body = request.POST.get('body')
        )
        return redirect('home')
    return render(request, 'fungus/add_post.html', context)

@login_required
def like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_objs = Post.objects.get(id = post_id)
        if request.user in post_objs.like_post.all():
            post_objs.like_post.remove(request.user)
        else:
            post_objs.like_post.add(request.user)
        like, created = Like.objects.get_or_create(user_like = request.user, post_likes=post_objs)
        like.save()
        return redirect('home')

@login_required
def dislike(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_objs = Post.objects.get(id = post_id)
        if request.user in post_objs.dislike_post.all():
            post_objs.dislike_post.remove(request.user)
        else:
            post_objs.dislike_post.add(request.user)
        dislike, created = Dislike.objects.get_or_create(user_dislike = request.user, post_dislikes=post_objs)
        dislike.save()
        return redirect('home')