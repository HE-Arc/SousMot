from django.contrib import admin

from .models import User, Dictionary, Word, Mode, Game, Games_per_users, History_solo
# Register your models here.

admin.site.register(User)
admin.site.register(Dictionary)
admin.site.register(Word)
admin.site.register(Mode)
admin.site.register(Game)
admin.site.register(Games_per_users)
admin.site.register(History_solo)