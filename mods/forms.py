from django import forms
from .models import Comment, Mod, ModVersion

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add a comment...',
                'id': 'comment'
            })
        }

class ModForm(forms.ModelForm):
    class Meta:
        model = Mod
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mod name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Mod description'}),
        }

class ModVersionForm(forms.ModelForm):
    class Meta:
        model = ModVersion
        fields = ['version_number', 'changelog', 'zip_file', 'private']
        widgets = {
            'version_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Version number'}),
            'changelog': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What’s new?'}),
            'zip_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
