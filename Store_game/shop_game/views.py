from sqlite3 import IntegrityError

from aiohttp.web_urldispatcher import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from .models import *



@login_required
def game_list(request):
    search_query = request.GET.get('search', '')
    games = Game.objects.filter(title__icontains=search_query)
    genre_name = request.GET.get('genre')
    profile = get_object_or_404(Profile, user=request.user)
    if genre_name:
        games = games.filter(genre__name=genre_name)
    sort_by = request.GET.get('sort', 'title')
    games = games.order_by(sort_by)
    return render(request, 'games/game_list.html', {'games': games, 'search_query': search_query, 'profile': profile})

@login_required
def rate_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == "POST":
        vote_type = request.POST.get('vote_type')
        rating, created = Rating.objects.get_or_create(user=request.user, game=game)
        rating.vote_type = vote_type
        rating.save()
        return redirect('game_detail', game_id=game.id)
    return HttpResponse(status=204)

@login_required
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    ratings = Rating.objects.filter(game=game)
    like_count = ratings.filter(vote_type='like').count()
    dislike_count = ratings.filter(vote_type='dislike').count()
    system_requirements = SystemRequirement.objects.filter(game=game)
    os = system_requirements.values_list('os', flat=True).first()
    cpu = system_requirements.values_list('cpu', flat=True).first()
    ram = system_requirements.values_list('ram', flat=True).first()
    storage = system_requirements.values_list('storage', flat=True).first()
    gpu = system_requirements.values_list('gpu', flat=True).first()
    context = {
        'game': game,
        'like_count': like_count,
        'dislike_count': dislike_count,
        'user_rating': ratings.filter(user=request.user).first(),
        'os': os,
        'cpu': cpu,
        'ram': ram,
        'storage': storage,
        'gpu': gpu
    }

    return render(request, 'games/game_detail.html', context)

@login_required
def buy_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    profile = get_object_or_404(Profile, user=request.user)

    if profile.money >= game.price:
        profile.money -= game.price
        profile.save()
        order = Order(user=request.user, game=game)
        order.save()
        return redirect('game_detail', game_id=game.id)  # Ваша детальная страница игры
    else:
        return redirect('game_detail', game_id=game.id)

@login_required
def support_ticket_view(request, game_id):
    if request.method == 'POST':
        subject = request.POST.get('subject_support')
        email = request.POST.get('email_support')
        message = request.POST.get('message_support')
        game = Game.objects.get(id=game_id)
        ticket = SupportTicket.objects.create(
            user=request.user,
            subject=subject,
            email=email,
            game=game,
            message=message
        )

        return redirect('game_detail', game_id=game_id)
    return render(request, 'support/support.html', {'game_id': game_id})

def register_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        avatar = request.FILES.get('avatar')

        try:
            if password1 == password2:
                user = User.objects.create_user(username=username, password=password1, email=email)

                if not avatar:
                    avatar = '../media/image_site/default_avatar.png'  # Укажите путь к вашей дефолтной аватарке

                profile = Profile.objects.create(user=user, avatar=avatar)
                profile.save()
                user = authenticate(request, username=username, password=password1)
                login(request, user)
                return redirect('game_list')
            else:
                return redirect('register')
        except IntegrityError:
            return redirect('register')
    return render(request, 'accounts/register.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('game_list')
        else:
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(user=request.user).first()
    return render(request, 'accounts/home.html', {'user': request.user, 'profile': profile, 'order': order})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')

@login_required
def add_balance(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        if amount > 0:
            profile = get_object_or_404(Profile, user=request.user)
            profile.money += amount
            profile.save()
            return redirect('add_balance')
        else:
            return redirect('add_balance')
    return render(request, 'accounts/add_balance.html', {'error': 'Введите корректную сумму'})

@login_required
def user_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = []
    return render(request, 'accounts/user_orders.html', {'orders': orders})

@login_required
def activate_code(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.is_active = True
    order.save()
    return redirect('user_orders')

@login_required
def refund_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    profile = get_object_or_404(Profile, user=request.user)
    if order.is_active:
        order.delete()
    elif not order.is_active:
        profile.money += order.game.price
        profile.save()
        order.delete()
    return redirect('user_orders')

@login_required
def edit_profile(request):
    user = get_object_or_404(User, username=request.user.username)
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        new_email = request.POST.get('new_email')
        new_avatar = request.FILES.get('new_avatar')
        password = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                return redirect('edit_profile')

            user.username = new_username
        if new_email and new_email != user.email:
            user.email = new_email
        if new_avatar:
            profile.avatar = new_avatar
        if password:
            if password == password2:
                user.set_password(password)
            else:
                return redirect('edit_profile')

        try:
            user.save()
            profile.save()
            login(request, user)
            return redirect('profile')
        except Exception as e:
            return redirect('edit_profile')
    return render(request, 'accounts/edit_profile.html', {'user': user, 'profile': profile})





