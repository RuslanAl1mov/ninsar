from django.contrib import admin
from .models import Competition, Room, Team, CompetitionResult

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    search_fields = ("name",)
    list_filter = ("start_date",)
    date_hierarchy = "start_date"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(CompetitionResult)
class CompetitionResultAdmin(admin.ModelAdmin):
    list_display = (
        "competition",
        "scenario",
        "user",
        "team",
        "room",
        "flight_time",
        "false_start",
    )
    list_filter = (
        "competition",
        "scenario",
        "team",
        "false_start",
    )
    search_fields = ("user__username", "team__name")
    autocomplete_fields = ("competition", "room", "team", "user")
    ordering = ("flight_time",)