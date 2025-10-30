from django.db import models
from django.contrib.auth.models import User

class Mod(models.Model):
    name = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class ModVersion(models.Model):
    mod = models.ForeignKey('Mod', on_delete=models.CASCADE)
    changelog = models.TextField()
    version_number = models.CharField(max_length=50)
    zip_file = models.FileField(upload_to='mods/')
    private = models.BooleanField(default=False)
    downloads = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.mod.name} - {self.version_number}"

class Comment(models.Model):
    mod = models.ForeignKey('Mod', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mod_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)