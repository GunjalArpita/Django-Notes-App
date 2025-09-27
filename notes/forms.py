from django import forms
from .models import Note, NoteFile

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

class NoteFileForm(forms.ModelForm):
    class Meta:
        model = NoteFile
        fields = ['file', 'name']
