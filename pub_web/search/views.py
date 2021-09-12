from typing import ContextManager
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def index(request):
    context = {
        'context': 'Hello World!'
    }
    return render(request, 'search/index.html', context)