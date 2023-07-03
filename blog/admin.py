from django.contrib import admin
from .models import Squad, News


class SquadAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


class NewsSquads(admin.ModelAdmin):
    list_display = ('squad', 'author', 'title', 'content', 'created_at', 'updated_at', 'slug')
    search_fields = ('squad', 'title')


admin.site.register(Squad, SquadAdmin)
admin.site.register(News, NewsSquads)
