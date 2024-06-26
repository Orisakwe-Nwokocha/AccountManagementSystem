from django.urls import path

from . import views

urlpatterns = [
    path('all', views.find_all),
    path('find/<str:account_number>', views.get_account),
    path('deposit', views.deposit),
]
