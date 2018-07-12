from django.shortcuts import render
from django.http import JsonResponse

from .preprocess_modules import *

def test_tokenize_ch(request):
    text = request.GET['text']
    tokens = tokenize_ch(text)
    data = {"Text": text, "Tokens": tokens}
    return JsonResponse({'test_tokenize_ch': data})
