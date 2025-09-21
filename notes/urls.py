from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_list, name='notes_list'),
    path('add/', views.add_note, name='add_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
        path('update/<int:note_id>/', views.update_note, name='update_note'),
            path('view/<int:note_id>/', views.view_note, name='view_note'),
]
