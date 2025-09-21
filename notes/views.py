from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Note
from django.contrib.auth.decorators import login_required

@login_required
def notes_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        notes = Note.objects.filter(user=request.user, title__icontains=search_query)
    else:
        notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/notes_list.html', {'notes': notes, 'request': request})

@login_required
def add_note(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content, user=request.user)
        return redirect('notes_list')
    return render(request, 'notes/add_note.html')

@login_required
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    note.delete()
    return redirect('notes_list')


@login_required
def update_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    if request.method == "POST":
        note.title = request.POST['title']
        note.content = request.POST['content']
        note.save()
        return redirect('notes_list')
    return render(request, 'notes/update_note.html', {'note': note})


@login_required
def view_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)
    return render(request, 'notes/view_note.html', {'note': note})
