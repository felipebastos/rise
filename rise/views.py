from players.models import Alliance
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'rise/index.html')


def logar(request):
    if request.method == 'GET':
        return render(request, 'rise/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            # Return an 'invalid login' error message.
            return redirect('/login')


@login_required
def sair(request):
    logout(request)
    return redirect('/')
