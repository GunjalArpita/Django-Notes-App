from django.db import models

# Create your models here.



from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_secret = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class NoteFile(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='note_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name or self.file.name
