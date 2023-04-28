import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from config.forms import ConfigForm, DestaqueFormSet
from config.models import SiteConfig

logger = logging.getLogger("k32")


# Create your views here.
@login_required
def home(request):
    config = SiteConfig.objects.all().first()
    if not config:
        logger.debug("Configuração inicial criada.")
        config = SiteConfig.objects.create()

    if request.method == "POST":
        form = ConfigForm(request.POST, instance=config)
        formset = DestaqueFormSet(request.POST, instance=config)

        if form.is_valid():
            form.save()
            logger.debug("%s alterou configuracoes gerais", request.user.username)

        if formset.is_valid():
            formset.save()
            logger.debug("%s alterou destaques do site", request.user.username)

    form = ConfigForm(instance=config)
    formset = DestaqueFormSet(instance=config)
    context = {
        "form": form,
        "destaqueform": formset,
    }

    return render(request, "config/index.html", context=context)
