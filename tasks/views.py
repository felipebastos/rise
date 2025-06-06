from importlib import import_module

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from tasks.forms import ConfiguraTask
from tasks.models import Task
from tasks.scripts.script import RiseTask


# Create your views here.
@login_required
def home(request):
    tasks = Task.objects.all()
    x = 2
    print(x)
    if request.method == "POST":
        form = ConfiguraTask(request.POST)
        if form.is_valid():
            nova_task: Task = form.save()
            modulo = import_module(
                f"tasks.scripts.{nova_task.script.split('.', maxsplit=1)[0]}"
            )
            script: RiseTask = modulo.main()
            nova_task.nome_da_task = script.nome
            nova_task.descricao = script.descricao
            nova_task.save()

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

    form = None
    if task.form_class() is not None:
        form = task.form_class()(request.POST or None)

    if task:
        request.session["resultado_task"] = {
            "nome": task.nome_da_task,
            "uuid": str(task.uuid),
            "mensagem": str(task.executar(form)),
        }

    return redirect(to=home)


@login_required
def remove_task(request, uuid):
    task = Task.objects.get(uuid=uuid)
    if task:
        task.delete()
    return redirect(to=home)
