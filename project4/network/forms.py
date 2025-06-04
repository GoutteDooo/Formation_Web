from django import forms

class PostForm(forms.Form):
    content = forms.CharField(label="New post", max_length=1000, widget=forms.Textarea)