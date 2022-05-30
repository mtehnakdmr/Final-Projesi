from django.urls import path
from home import views



urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('gallery/', views.myimages, name="myimages"),
    path('<str:imageURL>/', views.image, name="image")
]

handler404 = "views.handler404"