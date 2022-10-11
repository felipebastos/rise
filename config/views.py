from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from config.models import SiteConfig
from config.forms import ConfigForm

# Create your views here.
@login_required
def home(request):
    config = SiteConfig.objects.all().first()
    if not config:
        config = SiteConfig.objects.create()
    if request.method == "POST":
        form = ConfigForm(request.POST, instance=config)

        if form.is_valid():
            form.save()

    form = ConfigForm(instance=config)
    context = {
        "form": form,
    }

    return render(request, "config/index.html", context=context)
