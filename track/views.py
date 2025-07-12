from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def track_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'track_list.html')