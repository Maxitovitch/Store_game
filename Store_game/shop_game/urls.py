from django.urls import path
from .views import *

urlpatterns = [
    path('', login_page, name='login'),
    path('games/', game_list, name='game_list'),
    path('game/<int:game_id>/', game_detail, name='game_detail'),
    path('buy/<int:game_id>/', buy_game, name='buy_game'),
    path('game/<int:game_id>/support/', support_ticket_view, name='support_ticket'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout_view'),
    path('add_balance/', add_balance, name='add_balance'),
    path('user_orders/', user_orders, name='user_orders'),
    path('activate_code/<int:order_id>/', activate_code, name='activate_code'),
    path('refund_order/<int:order_id>/', refund_order, name='refund_order'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('rate_game/<int:game_id>/', rate_game, name='rate_game'),
]

