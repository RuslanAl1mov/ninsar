# Generated by Django 5.2.1 on 2025-05-24 15:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название соревнования')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Дата начала')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Дата окончания')),
            ],
            options={
                'verbose_name': 'Соревнование',
                'verbose_name_plural': 'Соревнования',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Комната (сессия)')),
            ],
            options={
                'verbose_name': 'Комната',
                'verbose_name_plural': 'Комнаты',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Название команды')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
            },
        ),
        migrations.CreateModel(
            name='CompetitionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scenario', models.CharField(choices=[('practice', 'Тренировка'), ('qualification', 'Квалификация'), ('final', 'Финал')], db_index=True, max_length=32, verbose_name='Сценарий')),
                ('flight_time', models.FloatField(help_text='Чем меньше, тем лучше', verbose_name='Время полёта (с)')),
                ('false_start', models.BooleanField(default=False, verbose_name='Фальстарт')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competitions_app.competition', verbose_name='Соревнование')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='competitions_app.room', verbose_name='Комната')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='competitions_app.team', verbose_name='Команда')),
            ],
            options={
                'verbose_name': 'Результат попытки',
                'verbose_name_plural': 'Результаты попыток',
                'ordering': ['flight_time', 'id'],
                'indexes': [models.Index(fields=['competition', 'scenario', 'flight_time'], name='competition_competi_eb9d19_idx')],
            },
        ),
    ]
