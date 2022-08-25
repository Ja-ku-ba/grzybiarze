from .models import Fung, Post, Like, Dislike, Room, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import User_form, Post_form
from django.contrib import messages



from django.db.models import Q
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
            if request.user in post_objs.dislike_post.all():
                post_objs.dislike_post.remove(request.user)
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
            if request.user in post_objs.like_post.all():
                post_objs.like_post.remove(request.user)
        dislike, created = Dislike.objects.get_or_create(user_dislike = request.user, post_dislikes=post_objs)
        dislike.save()
        return redirect('home')

def rooms_page(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'fungus/rooms_list.html', context)

def create_room(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        new_room = Room.objects.create(
            owner = request.user,
            topic = topic,
        )
        return redirect('room', new_room.id)
    return render(request, 'fungus/room_create.html')

def room_p(request, pk):
    room = Room.objects.get(id=pk)
    participants = room.participants.all()
    massages = room.message_set.all()
    context = {'room': room, 'massages':massages}
    if request.method == 'POST':
        body = request.POST.get('body')
        Message.objects.create(
            owner = request.user,
            room = room,
            body = body
        )
        room.participants.add(request.user)
        return redirect('room', room.id)
    return render(request, 'fungus/room.html', context)

def user_page(request, pk):
    user = User.objects.get(id=pk)
    messages = user.message_set.all()
    posts = Post.objects.filter(owner=pk)
    context = {'user':user, 'messages':messages, 'posts':posts}
    return render(request, 'fungus/user.html', context)

def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__icontains=q)
    )
    posts = Post.objects.filter(
        Q(body__icontains=q)
    )
    messages = Message.objects.filter(
        Q(body__icontains=q)
    )
    comb_res = rooms.count() + posts.count() + messages.count()
    context = {'rooms':rooms, 'posts':posts, 'messages':messages, 'comb_res':comb_res}
    return render(request, 'fungus/results.html', context)
