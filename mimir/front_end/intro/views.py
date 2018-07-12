from django import template
from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse

def intro_peculab(request):
    return render(request, 'intro/intro_peculab.html')

def intro_mimir(request):
    return render(request, 'intro/intro_mimir.html')