import logging
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from config.models import SiteConfig
from config.forms import ConfigForm, DestaqueFormSet

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
            logger.debug(
                f"{request.user.username} alterou configuracoes gerais"
            )

        if formset.is_valid():
            formset.save()
            logger.debug(f"{request.user.username} alterou destaques do site")

    form = ConfigForm(instance=config)
    formset = DestaqueFormSet(instance=config)
    context = {
        "form": form,
        "destaqueform": formset,
    }

    return render(request, "config/index.html", context=context)
