from datetime import datetime

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
def index(request: HttpRequest) -> HttpResponse:
    time = datetime.now()
    return HttpResponse(time.strftime('%A'))
# Create your views here.
