from django.urls import path
from . import views
urlpatterns = [
    path('',views.main_page, name='main_page'),
    path('createAccount/',views.sign_up, name='sign_up'),
    path('pin/',views.pin, name='pin'),
    path('home/',views.home, name='home'),
    path('deposit/',views.deposit, name='deposit'),
    path('withdrawl/',views.withdrawl, name='withdrawl'),
    path('transfer/',views.transfer, name='transfer'),
    path('balance/',views.balance, name='balance'),
    path('error/',views.err_or, name='error'),
    path('success/',views.succ_ess, name='success'),
    path('logout/',views.user_logout, name='logout'),
    
]