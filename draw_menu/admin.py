from django.contrib import admin
from .models import Item, Menu


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'href',)
    list_filter = ('title', 'href',)
    fieldsets = (
        ('Menu', {'fields': ('part_of',)}),
        ('Item', {'fields': ('title', 'href', 'parent',)}),
        ('Advanced', {'fields': ('seq', 'path',), 'classes': ('collapse',)}),
    )


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    fieldsets = (
        ('Create New Menu', {'fields': ('name',)}),
        ('Advanced', {'fields': ('seq',), 'classes': ('collapse',)}),
    )
