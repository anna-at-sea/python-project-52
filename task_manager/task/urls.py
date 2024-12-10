from django.urls import path
from task_manager.task import views

urlpatterns = [
    path('', views.TaskIndexView.as_view(), name='task_index'),
    path(
        'create/',
        views.TaskFormCreateView.as_view(),
        name='task_create'
    ),
    path(
        '<int:id>/update/',
        views.TaskFormUpdateView.as_view(),
        name='task_update'
    ),
    path(
        '<int:id>/delete/',
        views.TaskFormDeleteView.as_view(),
        name='task_delete'
    ),
    path(
        '<int:id>/',
        views.TaskPageView.as_view(),
        name='task_page'
    ),
]
