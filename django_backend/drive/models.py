from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='children'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name

    def get_path(self):
        path = []
        folder = self.parent
        while folder:
            path.insert(0, {'id': folder.id, 'name': folder.name})
            folder = folder.parent
        return path


def upload_to(instance, filename):
    folder_id = instance.folder.id if instance.folder else 'root'
    return f'files/{instance.user.id}/{folder_id}/{filename}'


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=upload_to)
    size = models.BigIntegerField(default=0)
    mime_type = models.CharField(max_length=100, blank=True)
    folder = models.ForeignKey(
        Folder, null=True, blank=True, on_delete=models.CASCADE, related_name='files'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name
