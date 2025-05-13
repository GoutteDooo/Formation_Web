from django.shortcuts import render
from django import forms

tasks = ["foo","bar","baz"]

class NewTaskForm(forms.Form):
  task = forms.CharField(label="new task")
# Create your views here.
def index(request):
  return render(request, "tasks/index.html", {
    "tasks": tasks
  })

def add(request):
  return render(request, "tasks/add.html", {
    "new task": NewTaskForm()
  })