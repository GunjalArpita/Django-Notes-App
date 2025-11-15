from django.conf import settings
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Note, NoteFile
from .forms import NoteForm, NoteFileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@login_required
def move_to_secret(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user, is_secret=False)
    note.is_secret = True
    note.save()
    request.session['move_message'] = f"Note '{note.title}' moved from Normal Notes to Secret Notes."
    return redirect('notes_list')

@login_required
def move_to_normal(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user, is_secret=True)
    note.is_secret = False
    note.save()
    request.session['move_message'] = f"Note '{note.title}' moved from Secret Notes to Normal Notes."
    return redirect('secrets_notes')
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Note, NoteFile
from .forms import NoteForm, NoteFileForm


@login_required
def delete_file(request, file_id, note_id):
    file_obj = NoteFile.objects.filter(id=file_id, note__user=request.user, note_id=note_id).first()
    if file_obj:
        # Delete the file from storage
        file_path = file_obj.file.path
        if os.path.exists(file_path):
            os.remove(file_path)
        file_obj.delete()
    # Check if the note is secret and redirect accordingly
    note = Note.objects.filter(id=note_id, user=request.user).first()
    if note and note.is_secret:
        return redirect('view_secret_note', note_id=note_id)
    return redirect('view_note', note_id=note_id)
@login_required
def view_secret_note(request, note_id):
    if not request.session.get('secrets_unlocked'):
        return HttpResponseRedirect(reverse('notes_list'))
    note = Note.objects.get(id=note_id, user=request.user, is_secret=True)
    return render(request, 'notes/view_secret_note.html', {'note': note})

@login_required
def edit_secret_note(request, note_id):
    if not request.session.get('secrets_unlocked'):
        return HttpResponseRedirect(reverse('notes_list'))
    note = Note.objects.get(id=note_id, user=request.user, is_secret=True)
    message = None
    if request.method == "POST":
        new_title = request.POST['title']
        new_content = request.POST['content']
        if new_title == note.title and new_content == note.content:
            message = "Nothing is changed."
        else:
            note.title = new_title
            note.content = new_content
            note.save()
            return HttpResponseRedirect(reverse('secrets_notes'))
    return render(request, 'notes/edit_secret_note.html', {'note': note, 'message': message})

@login_required
def delete_secret_note(request, note_id):
    if not request.session.get('secrets_unlocked'):
        return HttpResponseRedirect(reverse('notes_list'))
    note = Note.objects.get(id=note_id, user=request.user, is_secret=True)
    note.delete()
    return HttpResponseRedirect(reverse('secrets_notes'))

@login_required
def notes_list(request):
    search_query = request.GET.get('search', '')
    search_type = request.GET.get('search_type', 'text')
    sort_option = request.GET.get('sort', 'default')
    notes = Note.objects.filter(user=request.user, is_secret=False)
    if search_query:
        if search_type == 'title':
            notes = notes.filter(title__icontains=search_query)
        else:
            notes = notes.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

    if sort_option == 'date':
        notes = notes.order_by('created_at')
    elif sort_option == 'az':
        notes = notes.order_by('title')
    elif sort_option == 'za':
        notes = notes.order_by('-title')
    else:
        notes = notes.order_by('-created_at')  # default: newest first

    move_message = request.session.pop('move_message', None)
    return render(request, 'notes/notes_list.html', {'notes': notes, 'request': request, 'move_message': move_message})

@login_required
def add_note(request):
    if request.method == "POST":
        note_form = NoteForm(request.POST)
        files = request.FILES.getlist('files')
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.user = request.user
            note.save()
            for f in files:
                NoteFile.objects.create(note=note, file=f, name=f.name)
            return redirect('notes_list')
    else:
        note_form = NoteForm()
    return render(request, 'notes/add_note.html', {'note_form': note_form})

@login_required
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    note.delete()
    return redirect('notes_list')


@login_required
def update_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    message = None
    if request.method == "POST":
        new_title = request.POST['title']
        new_content = request.POST['content']
        if new_title == note.title and new_content == note.content:
            message = "Nothing is changed."
        else:
            note.title = new_title
            note.content = new_content
            note.save()
            return redirect('notes_list')
    return render(request, 'notes/update_note.html', {'note': note, 'message': message})


@login_required
def view_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    return render(request, 'notes/view_note.html', {'note': note})


def secrets_auth(request):
    if request.method == 'POST':
        password = request.POST.get('secrets_password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            request.session['secrets_unlocked'] = True
            return HttpResponseRedirect(reverse('secrets_notes'))
        else:
            return render(request, 'notes/secrets_auth_failed.html')
    return render(request, 'notes/secrets_auth.html')


@login_required
def secrets_notes(request):
    if not request.session.get('secrets_unlocked'):
        return HttpResponseRedirect(reverse('notes_list'))
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content, user=request.user, is_secret=True)
        return HttpResponseRedirect(reverse('secrets_notes'))
    secret_notes = Note.objects.filter(user=request.user, is_secret=True)
    move_message = request.session.pop('move_message', None)
    return render(request, 'notes/secrets_notes.html', {'secret_notes': secret_notes, 'move_message': move_message})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('login')
            except Exception as e:
                error_message = f"Error during registration: {e}"
                return render(request, 'registration/registration.html', {'form': form, 'error': error_message})
        else:
            error_message = "Form validation failed. Please correct the errors below."
            return render(request, 'registration/registration.html', {'form': form, 'error': error_message})
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'notes/profile.html', {
        'username': request.user.username,
        'email': request.user.email,
    })
