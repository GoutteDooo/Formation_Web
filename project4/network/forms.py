from django import forms

class PostForm(forms.Form):
    content = forms.CharField(
        label="",
        max_length=1000,
        min_length=5,
        widget=forms.Textarea(attrs={
            'placeholder': 'How are you feeling today?',
            'rows':3
        })
    )
