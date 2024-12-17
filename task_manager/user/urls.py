from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='user_index'),
    path(
        'create/',
        views.UserFormCreateView.as_view(),
        name='user_create'
    ),
    path(
        '<int:pk>/update/',
        views.UserFormUpdateView.as_view(),
        name='user_update'
    ),
    path(
        '<int:pk>/delete/',
        views.UserFormDeleteView.as_view(),
        name='user_delete'
    ),
]
