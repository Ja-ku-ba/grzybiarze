from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('atlas', views.atlas, name='atlas'),
    path('atlas/<str:pk>', views.munschrom_page, name='munschrom_page'),

    path('wyniki-wyszukiwania', views.search, name='search'),

    path('pokoje', views.rooms_page, name='rooms_page'),
    path('stworz-pokoj', views.create_room, name='create_room'),
    path('pokoj/<str:pk>', views.room_p, name='room'),
    path('usun-pokoj/<str:pk>', views.delete_room, name='delete_room'),
    path('ukryj-wiadomosc/<str:pk>', views.hide_message, name='hide_message'),

    path('zarejestruj', views.register, name='register'),
    path('zaloguj', views.user_login, name='user_login'),
    path('wyloguj', views.user_logout, name='user_logout'),
    path('uzytkownik/<str:pk>', views.user_page, name='user'),

    path('zapostuj', views.add_post, name='add_post'),
    path('like', views.like, name='like'),
    path('dislike', views.dislike, name='dislike'),
]