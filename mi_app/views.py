from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    return HttpResponse("Hola desde Django en Codespaces")

# Create your views here.
