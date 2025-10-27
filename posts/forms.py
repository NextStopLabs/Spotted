from django import forms
from .models import Post

# ✅ Custom widget that supports multiple file uploads
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class PostForm(forms.ModelForm):
    files = forms.FileField(
        widget=MultiFileInput(attrs={
            'multiple': True,
            'class': 'form-control-file'
        }),
        required=False,
        label='Upload Files'
    )

    class Meta:
        model = Post
        fields = ['title', 'description', 'tags', 'files']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write something...'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'bus, train, spotting...'}),
        }
