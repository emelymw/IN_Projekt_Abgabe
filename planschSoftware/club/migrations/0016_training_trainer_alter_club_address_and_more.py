# Generated by Django 4.1.3 on 2023-08-05 22:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('club', '0015_alter_attendance_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='club.trainer', verbose_name='Trainer'),
        ),
        migrations.AlterField(
            model_name='club',
            name='address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='club.address', verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='departmentmanager',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='swimmer',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='club.swimmgroup', verbose_name='Schwimmgruppe'),
        ),
        migrations.AlterField(
            model_name='swimmgroup',
            name='main_trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='main_trainer', to='club.trainer', verbose_name='Haupttrainer'),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
