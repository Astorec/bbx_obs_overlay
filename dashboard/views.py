from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import SettingsForm
from .models import Settings, Tournaments, Matches, Participants
import challonge

def Dashboard(request):
    settings = Settings.objects.first()
    fetch_challonge_data(settings.api_key, settings.username)
    tournament = Tournaments.objects.first()
    rounds = list(set(match.round for match in Matches.objects.all()))

    return render(request, 'dashboard/home.html', {'tournament': tournament, 'rounds': rounds})

def test_func(request):
    print("\ntest func")
    return HttpResponse("""""")

def ChallongeSettings(request):
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            # Check to see if we have data in the DB already
            if Settings.objects.count() == 0:
                # If not, create a new object
                form.save()
            else:
                # Remove any existing data on the Table so we can overwite it with the new data
                # that was entered by the user
                settings = Settings.objects.all()
                settings.delete()
                
                # Once done we then save the newly entered data
                form.save() 
                
            return redirect("/")
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = SettingsForm()
    return render(request, 'dashboard/settings.html', {'form': form})

def fetch_challonge_data(api_key, username):
    challonge.set_credentials( username, api_key)
    get_tournament = challonge.tournaments.show("pn120ezw")
    
    tournament, created = Tournaments.objects.get_or_create(tournament_id=get_tournament["id"], defaults={
        'name': get_tournament["name"],
        'description': get_tournament["description"],
        'created_at': get_tournament["created_at"],
        'state': get_tournament["state"],
        'swiss_rounds': get_tournament["swiss_rounds"],
        'started_at': get_tournament["started_at"],
        'start_at': get_tournament["start_at"],
        'participants_locked': get_tournament["participants_locked"],
        'participants_swappable': get_tournament["participants_swappable"]
    })
    
    get_matches = challonge.matches.index("pn120ezw")
    
    for match in get_matches:
        match, created = Matches.objects.get_or_create(match_id=match["id"], defaults={
            'identifier': match["identifier"],
            'player1_id': match["player1_id"],
            'player2_id': match["player2_id"],
            'state': match["state"],
            'round': match["round"],
            'loser_id': match["loser_id"],
            'group_id': match["group_id"],
            'tournament_id': match["tournament_id"]
        })
        
    get_participants = challonge.participants.index("pn120ezw")
    
    for participant in get_participants:
        participant, created = Participants.objects.get_or_create(participant_id=participant["id"], defaults={
            'group_id': participant["group_id"],
            'name': participant["name"],
            'tournament_id': participant["tournament_id"],
            'challonge_username': participant["challonge_username"],
            'username': participant["username"]
        })
        
def get_matches_for_round(request, tournament_id, round_number):
    matches = Matches.objects.filter(tournament_id=tournament_id, round=round_number)
    matches_data = list(matches.values()) 
    return JsonResponse(matches_data, safe=False)

def get_participant_for_match(request, tournament_id, player_id):
        
    participants = Participants.objects.filter(tournament_id=tournament_id, participant_id=player_id)
    participants_data = list(participants.values())
    return JsonResponse(participants_data, safe=False)
        
   