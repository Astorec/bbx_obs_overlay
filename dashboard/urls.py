from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('settings', views.ChallongeSettings, name='settings'),
    path('api/matches/<int:tournament_id>/<int:round_number>/', views.get_matches_for_round, name='get_matches_for_round'),
    path('api/participants/<int:tournament_id>/<int:player_id>/', views.get_participant_for_match, name='get_participant_for_match'),
    path('connect_to_obsws/', views.connect_to_obsws, name='connect_to_obsws'),
    path('send_players_to_obs/', views.send_player_to_obs, name='send_players_to_obs'),
]