from django import forms

class PostForm(forms.Form):
  content = forms.CharField(label="New post", max_length=1000, place_holder="How are you feeling today ?", widget=forms.Textarea)