from django.contrib import admin
from .models import UserInfo, Team, Player

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Player)
admin.site.register(Team)
