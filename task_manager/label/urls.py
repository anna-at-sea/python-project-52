from django.urls import path
from task_manager.label import views

urlpatterns = [
    path('', views.LabelIndexView.as_view(), name='label_index'),
    path(
        'create/',
        views.LabelFormCreateView.as_view(),
        name='label_create'
    ),
    path(
        '<int:id>/update/',
        views.LabelFormUpdateView.as_view(),
        name='label_update'
    ),
    path(
        '<int:id>/delete/',
        views.LabelFormDeleteView.as_view(),
        name='label_delete'
    ),
]
