from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'Users/index.html')

def login(request):
	return render(request, 'Users/login.html')

def register(request):
	return render(request, 'Users/register.html')

def validation(request):
	pass