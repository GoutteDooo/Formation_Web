from django import forms

class PostForm(forms.Form):
    content = forms.CharField(
        label="New post",
        max_length=1000,
        widget=forms.Textarea(attrs={
            'placeholder': 'How are you feeling today?',
            'rows': 6,  # Optional: control height
            'cols': 50  # Optional: control width
        })
    )
