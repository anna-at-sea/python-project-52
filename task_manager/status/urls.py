from django.urls import path
from task_manager.status import views

urlpatterns = [
    path('', views.StatusIndexView.as_view(), name='status_index'),
    path(
        'create/',
        views.StatusFormCreateView.as_view(),
        name='status_create'
    ),
    path(
        '<int:pk>/update/',
        views.StatusFormUpdateView.as_view(),
        name='status_update'
    ),
    path(
        '<int:pk>/delete/',
        views.StatusFormDeleteView.as_view(),
        name='status_delete'
    ),
]
