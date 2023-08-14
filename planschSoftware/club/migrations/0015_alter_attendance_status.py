# Generated by Django 4.1.3 on 2023-07-29 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0014_alter_training_training_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('ANWESEND', 'a'), ('ENTSCHULDIGT', 'e'), ('UNENTSCHULDIGT', 'u'), ('UNBEKANNT', 'x')], default='UNBEKANNT', max_length=20, verbose_name='Anwesenheit'),
        ),
    ]
