from django.contrib import admin
from .models import Participants, Tournaments, Matches, Settings

admin.site.register(Participants)
admin.site.register(Tournaments)
admin.site.register(Matches)
admin.site.register(Settings)