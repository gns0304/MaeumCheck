from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    return render(request, 'login.html')

@login_required
def index(request):
    return render(request, 'index.html')