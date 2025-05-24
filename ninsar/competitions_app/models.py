from django.conf import settings
from django.db import models


class Competition(models.Model):
    name = models.CharField("Название соревнования", max_length=128, unique=True)
    start_date = models.DateField("Дата начала", null=True, blank=True)
    end_date = models.DateField("Дата окончания", null=True, blank=True)

    class Meta:
        verbose_name = "Соревнование"
        verbose_name_plural = "Соревнования"

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField("Комната (сессия)", max_length=64)

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField("Название команды", max_length=128, unique=True)

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        return self.name


class FlightScenario(models.TextChoices):
    PRACTICE = "practice", "Тренировка"
    QUALIFICATION = "qualification", "Квалификация"
    FINAL = "final", "Финал"


class CompetitionResult(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name="Соревнование")
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Комната")
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.PROTECT, verbose_name="Команда")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")

    scenario = models.CharField("Сценарий", max_length=32, choices=FlightScenario.choices, db_index=True)
    flight_time = models.FloatField("Время полёта (с)", help_text="Чем меньше, тем лучше")
    false_start = models.BooleanField("Фальстарт", default=False)

    class Meta:
        indexes = [models.Index(fields=["competition", "scenario", "flight_time"])]
        ordering = ["flight_time", "id"]
        verbose_name = "Результат попытки"
        verbose_name_plural = "Результаты попыток"

    def __str__(self):
        return f"{self.competition} | {self.user} | {self.flight_time:.3f}s"