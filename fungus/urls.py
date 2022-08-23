from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('atlas', views.atlas, name='atlas'),
    path('atlas/<str:pk>', views.munschrom_page, name='munschrom_page'),

    path('pokoje', views.rooms_page, name='rooms_page'),
    path('pokoj/<str:pk>', views.room_p, name='room'),

    path('zarejestruj', views.register, name='register'),
    path('zaloguj', views.user_login, name='user_login'),
    path('wyloguj', views.user_logout, name='user_logout'),
    path('uzytkownik/<str:pk>', views.user_page, name='user'),

    path('zapostuj', views.add_post, name='add_post'),
    path('like', views.like, name='like'),
    path('dislike', views.dislike, name='dislike'),
]