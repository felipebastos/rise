from datetime import date

from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    return render(request, 'kvk/index.html')