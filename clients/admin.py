from django.contrib import admin

from .models import CustomUser, Match


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'avatar', 'gender', 'first_name', 'last_name', 'email',
                    'password', 'lat', 'lon')


class MatchAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'user_like')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Match, MatchAdmin)
