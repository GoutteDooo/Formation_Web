from django.shortcuts import render
from django import forms

tasks = ["foo","bar","baz"]

class NewTaskForm(forms.Form):
  task = forms.CharField(label="New Task")
  priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)
# Create your views here.
def index(request):
  return render(request, "tasks/index.html", {
    "tasks": tasks
  })

def add(request):
  if request.method == "POST":
    form = NewTaskForm(request.POST)
  return render(request, "tasks/add.html", {
    "form": NewTaskForm()
  })