from django.urls import path
from .views import CreateUser, ViewUsers

urlpatterns = [
    path('', CreateUser.as_view(), name='user-create'),
    path('list/', ViewUsers.as_view(), name='user-list'),
]
