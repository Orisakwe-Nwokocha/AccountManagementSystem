from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('all', views.AccountViewSet)
print(router.urls)

urlpatterns = [
    # path('all', views.AccountViewSet.as_view({'get': 'list'})),
    # path('find/<str:pk>', views.AccountViewSet.as_view({'get': 'find', 'put': 'update', 'delete': 'delete'})),
    path('', include(router.urls)),
    path('deposit', views.Deposit.as_view()),
    path('withdraw', views.Withdraw.as_view()),
]



