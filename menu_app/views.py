from django.shortcuts import render
from django.http.request import HttpRequest

def base_view(request: HttpRequest):
    return render(request, 'menu/test.html')
