from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.notes_list, name='notes_list'),
    path('add/', views.add_note, name='add_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
        path('update/<int:note_id>/', views.update_note, name='update_note'),
            path('view/<int:note_id>/', views.view_note, name='view_note'),
    path('move_to_secret/<int:note_id>/', views.move_to_secret, name='move_to_secret'),
    path('view_secret/<int:note_id>/', views.view_secret_note, name='view_secret_note'),
    path('move_to_normal/<int:note_id>/', views.move_to_normal, name='move_to_normal'),
    path('secrets_auth/', views.secrets_auth, name='secrets_auth'),
    path('secrets_notes/', views.secrets_notes, name='secrets_notes'),
    path('edit_secret_note/<int:note_id>/', views.edit_secret_note, name='edit_secret_note'),
    path('delete_secret_note/<int:note_id>/', views.delete_secret_note, name='delete_secret_note'),
    path('delete_file/<int:file_id>/<int:note_id>/', views.delete_file, name='delete_file'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
]
