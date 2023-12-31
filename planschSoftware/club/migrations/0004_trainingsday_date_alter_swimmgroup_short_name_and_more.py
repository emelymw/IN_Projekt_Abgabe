# Generated by Django 4.1.3 on 2023-07-17 19:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0003_alter_swimmer_attest_alter_task_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingsday',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Startzeit'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='swimmgroup',
            name='short_name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Kürzel'),
        ),
        migrations.AlterField(
            model_name='task',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Kommentar'),
        ),
        migrations.AlterField(
            model_name='task',
            name='intensiity',
            field=models.CharField(blank=True, choices=[('loc', 'loc'), ('GA1', 'GA1'), ('GA2', 'GA2'), ('WSA', 'WSA'), ('sprint', 'sprint')], max_length=100, verbose_name='Intensität'),
        ),
        migrations.AlterField(
            model_name='task',
            name='number_parts',
            field=models.IntegerField(default=1, verbose_name='Wiederholungen'),
        ),
        migrations.AlterField(
            model_name='task',
            name='part_distance',
            field=models.IntegerField(verbose_name='Teilstrecke'),
        ),
        migrations.AlterField(
            model_name='task',
            name='part_task',
            field=models.TextField(verbose_name='Aufgabe'),
        ),
        migrations.AlterField(
            model_name='task',
            name='tools',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Hilfsmittel'),
        ),
        migrations.AlterField(
            model_name='task',
            name='total_distance',
            field=models.IntegerField(blank=True, null=True, verbose_name='Distanz'),
        ),
        migrations.AlterField(
            model_name='training',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trainingsday',
            name='end_time',
            field=models.TimeField(verbose_name='Endzeit'),
        ),
        migrations.AlterField(
            model_name='trainingsday',
            name='start_time',
            field=models.TimeField(verbose_name='Startzeit'),
        ),
    ]
