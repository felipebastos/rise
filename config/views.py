from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from config.models import SiteConfig
from config.forms import ConfigForm, DestaqueFormSet

# Create your views here.
@login_required
def home(request):
    config = SiteConfig.objects.all().first()
    if not config:
        config = SiteConfig.objects.create()

    if request.method == "POST":
        form = ConfigForm(request.POST, instance=config)
        formset = DestaqueFormSet(request.POST, instance=config)

        if form.is_valid():
            form.save()

        if formset.is_valid():
            formset.save()

    form = ConfigForm(instance=config)
    formset = DestaqueFormSet(instance=config)
    context = {
        "form": form,
        "destaqueform": formset,
    }

    return render(request, "config/index.html", context=context)
