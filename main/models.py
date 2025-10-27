from django.db import models

class FeatureToggle(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_coming_soon = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {'Enabled' if self.is_enabled else 'Disabled'}"