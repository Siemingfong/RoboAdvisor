from django.shortcuts import render
from django.http import JsonResponse

def me(request):
    return render(request, 'mimir/mimir_me.html')
