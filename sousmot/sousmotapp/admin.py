from django.contrib import admin

from .models import User, Dictionary, Word, Mode, Game, GamesPerUsers, HistorySolo
# Register your models here.

admin.site.register(User)
admin.site.register(Dictionary)
admin.site.register(Word)
admin.site.register(Mode)
admin.site.register(Game)
admin.site.register(GamesPerUsers)
admin.site.register(HistorySolo)