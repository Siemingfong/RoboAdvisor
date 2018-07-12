from django.shortcuts import render
from django.http import JsonResponse

from .analyze_modules import *

def test(request):
    # print('jaa')
    data = 'jaaaa'
    return JsonResponse({'test': data})
