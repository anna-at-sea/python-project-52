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
        '<int:id>/update/',
        views.StatusFormUpdateView.as_view(),
        name='status_update'
    ),
    path(
        '<int:id>/delete/',
        views.StatusFormDeleteView.as_view(),
        name='status_delete'
    ),
]
