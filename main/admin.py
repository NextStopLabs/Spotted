from django.contrib import admin
from .models import FeatureToggle

# Register your models here.
@admin.register(FeatureToggle)
class FeatureToggleAdmin(admin.ModelAdmin):
    """Admin interface for managing feature toggles."""
    list_display = ('name', 'is_coming_soon', 'is_enabled')
    list_editable = ('is_coming_soon', 'is_enabled')
    search_fields = ('name',)