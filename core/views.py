from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .services import PlayerRecommendation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

player_rec = PlayerRecommendation()
player_rec.initialize()

def index(request):
    return HttpResponse("Hello World")

def get_player_recommendation(request, player_id):
    
    recommendation_data = player_rec.find_player_neighbors(player_id)
    context = json.loads(recommendation_data)
    return render(request, 'players/index.html', context)

def players(request):

    players = player_rec.get_all_players()
    players_per_page = 10
    paginator = Paginator(players, players_per_page)

    # Obtenha o número da página da solicitação GET
    page = request.GET.get('page')

    try:
        # Obtenha os jogadores para a página atual
        players_for_page = paginator.page(page)
    except PageNotAnInteger:
        # Se o parâmetro da página não for um número inteiro, exiba a primeira página
        players_for_page = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, exiba a última página disponível
        players_for_page = paginator.page(paginator.num_pages)

    # Passe os dados paginados para o modelo usando o argumento 'context'
    context = {'players': players_for_page}

    # Use o método render para renderizar a página com os dados
    return render(request, 'players/test.html', context)