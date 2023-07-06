from django.urls import path
from app_login import views

urlpatterns = [
    path('login/', views.form_login, name='login'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('redefinePassword/<int:user_id>/<slug:reset_code>/', views.redefinePassword, name='redefinePassword'),
    path('register/', views.form_register, name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('account/', views.account, name='account'),
    path('logout/', views.form_logout, name='logout'),
    path('deleteAccount/', views.form_deleteAccount, name='deleteAccount'),
]
