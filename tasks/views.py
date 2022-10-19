from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from tasks.forms import ConfiguraTask

from tasks.models import Task

# Create your views here.
@login_required
def home(request):
    tasks = Task.objects.all()

    if request.method == "POST":
        form = ConfiguraTask(request.POST)
        if form.is_valid():
            form.save()

    mensagem = ""
    if "resultado_task" in request.session:
        mensagem = request.session["resultado_task"]
        del request.session["resultado_task"]

    context = {"tasks": tasks, "mensagem": mensagem}

    form = ConfiguraTask()
    context["form"] = form

    return render(request, "tasks/index.html", context=context)


@login_required
def execute_task(request, uuid):
    task = Task.objects.get(uuid=uuid)

    if task:
        request.session["resultado_task"] = {
            "nome": task.nome_da_task,
            "uuid": str(task.uuid),
            "mensagem": task.executar(),
        }

    return redirect(to=home)


@login_required
def remove_task(request, uuid):
    task = Task.objects.get(uuid=uuid)
    if task:
        task.delete()
    return redirect(to=home)
