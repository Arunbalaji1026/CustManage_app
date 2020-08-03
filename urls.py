from django.contrib import admin
from django.urls import path

from django.contrib.auth import views as auth_views
from .import views


urlpatterns= [
path('',views.home, name="home"),
path('product/',views.product, name="product"),
path('vendor/<str:pk_test>/',views.vendor, name="vendor"),
path('create_Order/',views.createOrder, name="create_Order"),
path('update_Order/<str:pk>/',views.updateOrder, name="update_Order"),
path('delete_Order/<str:pk>/',views.deleteOrder, name="delete_Order"),
path('login_page', views.loginPage, name="login_page"),
path('user_page', views.userpage, name="user_page"),
path('logout_user', views.logoutuser, name = "logout_user"),
path('registration_page', views.registrationPage, name="registration_page"),

path('reset_password',auth_views.PasswordResetView.as_view(), name="reset_password"),
path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(), name ="password_reset_done"),
path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(), name ="passowrd_reset_complete"),


]
