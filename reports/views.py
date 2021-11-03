from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Max, Min
from django.shortcuts import render

from datetime import date

from players.models import Alliance, PlayerStatus

# Create your views here.
@login_required
def index(request):
    aliancas = Alliance.objects.all()
    context = {
        'alliances': aliancas
    }
    
    if request.method == 'POST':
        try:
            universo = request.POST['universo']
            inicio = request.POST['inicio']
            fim = request.POST['fim']
            ordem = request.POST['ordem']

            context['inicio'] = date.fromisoformat(inicio)
            context['fim'] = date.fromisoformat(fim)

            ord = ''
            if ordem == 'kp':
                ord = '-kp'
                context['titulo'] = f'Ranking por Killpoints de {universo}'
            else:
                ord = '-dt'
                context['titulo'] = f'Ranking por Mortes de {universo}'

            #print(f'Procurando para {universo} entre {inicio} e {fim}, ordenado por {ordem}')
            status = None
            if universo == 'K32':
                status = PlayerStatus.objects.all().filter(data__gte=inicio).filter(data__lte=fim).values('player__nick').annotate(kp=Max('killpoints')-Min('killpoints'), dt=Max('deaths')-Min('deaths')).order_by(ord)
            else:
                status = PlayerStatus.objects.all().filter(player__alliance__tag=universo).filter(data__gte=inicio).filter(data__lte=fim).values('player__nick').annotate(kp=Max('killpoints')-Min('killpoints'), dt=Max('deaths')-Min('deaths')).order_by(ord)
            
            context['rank'] = status
        except Exception:
            pass
    
    return render(request, 'reports/index.html', context=context)

@login_required
def top300(request):    
    oReino = PlayerStatus.objects.exclude(player__alliance__tag='MIGR').exclude(player__status='INATIVO').order_by('-data')

    oReinoUnico = {}
    for status in oReino:
        if status.player.game_id not in oReinoUnico.keys():
            oReinoUnico[status.player.game_id] = status
    
    os300 = list(oReinoUnico.values())
    os300.sort(key=lambda x: x.power if(
        x is not None) else 0, reverse=True)
    os300 = os300[:300]

    poder = 0
    for p in os300:
        poder += p.power

    context = {
        'jogadores': os300,
        'poder': poder
    }
    return render(request, 'reports/top300.html', context=context)