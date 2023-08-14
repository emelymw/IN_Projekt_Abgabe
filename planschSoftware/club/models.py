from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Address(models.Model):
    """
    Speichert eine Adresse mit Postleitzahl, Stadt, Straße und Hausnummer.
    """
    postcode = models.CharField(max_length=10, verbose_name='Postleitzahl')
    city_name = models.CharField(max_length=200, verbose_name='Stadt')
    street_name = models.CharField(max_length=200, verbose_name='Straße')
    house_number = models.CharField(max_length=10, verbose_name='Hausnummer')

    def __str__(self):
        """
        Gibt das Objekt der Klasse als Text im Format '12345 Musterstadt, Musterstraße 1' zurück.
        :return: String
        """
        return f'{self.postcode} {self.city_name}, \n {self.street_name} {self.house_number}'

class DepartmentManager(models.Model):
    """
    Speichert einen Abteilungsleiter mit :model:`auth.User` und Email.
    """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name='User')
    email = models.EmailField(verbose_name='Email')

    def __str__(self):
        """
        Gibt das Objekt der Klasse als Text im Format 'Max Mustermann - max@mustermann.de' zurück.
        :return: String
        """
        return f'{self.user.first_name} {self.user.last_name} - {self.email}'

    def delete(self, *args, **kwargs):
        """
        Wird aufgerufen wenn das Objekt der KLasse gelöscht werden soll.
        Zuerst wir der :model:`auth.User` Account gelöscht und anschließend die normale delete Funktion aufgerufen.
        :param args: args
        :param kwargs: kwargs
        :return: super().delete()
        """
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

class Club(models.Model):
    """
    Speichert einen Verein mit Id, Name, kurzer Name, Abteilung und :model:`club.address`.
    """
    id = models.CharField(max_length=200, unique=True, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=200, verbose_name='Name')
    short_name = models.CharField(max_length=100, verbose_name='Kurzer Name')
    department = models.CharField(max_length=200, verbose_name='Abteilung')
    address = models.OneToOneField(Address, on_delete=models.PROTECT, verbose_name='Adresse')

    def __str__(self):
        """
        Gibt das Objekt der Klasse als Text im Format 'SG Musterstadt Schwimmen' zurück.
        :return: String
        """
        return f'{self.short_name} {self.department}'

class Trainer(models.Model):
    """
    Speichert einen Trainer mit :model:`auth.User`, Geburtstag, Ausbildung und Ablaufdatum vom Erste Hilfe und Rettungsschwimmer.
    """
    CHOICES = (
        ('Keine', 'Keine'),
        ('Junior-Trainer', 'Junior-Trainer'),
        ('Trainerassistent', 'Trainerassistent'),
        ('C-Trainer', 'C-Trainer'),
        ('B-Trainer', 'B-Trainer'),
    )

    user = models.OneToOneField(User, on_delete=models.SET_NULL, verbose_name='User', null=True)
    birth_date = models.DateField(blank=True, null=True, verbose_name='Geburtstag')
    education = models.CharField(max_length=200, choices=CHOICES, verbose_name='Status')
    expiry_date_first_aid = models.DateField(verbose_name='Ablaufdatum Erste Hilfe')
    expiry_date_lifeguard = models.DateField(verbose_name='Ablaufdatum Rettungsschwimmer')

    def __str__(self):
        """
        Gibt das Objekt der Klasse als Text im Format 'Max Mustermann' zurück.
        :return: String
        """
        return f'{self.user.first_name} {self.user.last_name}'

    def get_url(self):
        """
        Gibt die URL für die Detailseite des Trainers zurück.
        :return: url
        """
        return reverse('trainer-detail', args=[self.user.username])
    
    def delete(self, *args, **kwargs):
        """
        Wird aufgerufen wenn das Objekt der KLasse gelöscht werden soll.
        Zuerst wir der :model:`auth.User` Account gelöscht und anschließend die normale delete Funktion aufgerufen.
        :param args: args
        :param kwargs: kwargs
        :return: super().delete()
        """
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

class SwimmGroup(models.Model):
    """
    Speichert eine Schwimmgruppe mit kurzem Namen, Namen, Beschreibung, Altersgruppe, Wettkampfteilnahme, Haupttrainer
    und eventuell weiteren Trainern.
    """
    short_name = models.CharField(max_length=200, unique=True, verbose_name='Kürzel')
    name = models.CharField(max_length=200, verbose_name='Name')
    description = models.CharField(max_length=500, verbose_name='Beschreibung')
    age_group = models.CharField(max_length=200, verbose_name='Altergruppe')
    competition_participation = models.BooleanField(default=False, verbose_name='Wettkampfteilnahme')
    main_trainer = models.ForeignKey(Trainer, on_delete=models.PROTECT, related_name='main_trainer', verbose_name='Haupttrainer')
    trainer = models.ManyToManyField(Trainer, related_name='trainer', blank=True, verbose_name='Zusätzliche Trainer')

    def __str__(self):
        """
        Gibt das Objekt der Klasse als Text im Format 'Leistungsgruppe' zurück.
        :return: String
        """
        return f'{self.name}'

    def get_absolute_url(self):
        """
        Gibt die URL für die Detailseite der Schwimmgruppe zurück.
        :return: url
        """
        return reverse('swimmgroup-detail', args=[str(self.id)])

class TrainingsDay(models.Model):
    """
    Speichert einen Trainingstag mit :model:`club.SwimmGroup`, Datum, Startuhrzeit und Enduhrzeit.
    """
    swimm_group = models.ForeignKey(
        SwimmGroup, on_delete=models.CASCADE
    )
    date = models.DateField(verbose_name='Datum')
    start_time = models.TimeField(verbose_name='Startzeit')
    end_time = models.TimeField(verbose_name='Endzeit')

    def __str__(self):
        """
        Gibt das Objekt der Klasse als Text im Format '19:00 - 20:30' zurück.
        :return: String
        """
        return f'{self.start_time} - {self.end_time}'

class Swimmer(models.Model):
    """
    Speichert einen Schwimmer mit DSV_ID, Vorname, Nachname, Geburtstag, Email, :model:`club.SwimmGroup` und
    optional einem Attestdatum.
    """
    dsv_id = models.CharField(max_length=200, unique=True, primary_key=True, verbose_name='DSV-ID')
    first_name = models.CharField(max_length=200, verbose_name='Vorname')
    last_name = models.CharField(max_length=200, verbose_name='Nachname')
    birth_date = models.DateField(verbose_name='Geburtstag')
    attest = models.DateField(blank=True, null=True, verbose_name='Datum Attestausstellung')
    email = models.EmailField(verbose_name='Email')
    group = models.ForeignKey(SwimmGroup, on_delete=models.PROTECT, verbose_name='Schwimmgruppe')

    def __str__(self):
        """
        Gibt das Objekt der Klasse als Text im Format 'Max Mustermann' zurück.
        :return: String
        """
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        """
        Gibt die URL für die Detailseite des Schwimmers zurück.
        :return: url
        """
        return reverse('swimmer-detail', args=[str(self.dsv_id)])

class Trainingplan(models.Model):
    """
    Speichert einen Trainingsplan mit :model:`club.SwimmGroup`, Name, insgesamter Distanz und Kategorie.
    """
    CATEGORYS = [
        ("AUSDAUER", "Ausdauer"),
        ("SPRINT", "Sprint"),
        ("GEMISCHT", "Gemischt"),
    ]
    group = models.ForeignKey(SwimmGroup, on_delete=models.CASCADE, verbose_name='Schwimmgruppe')
    name = models.CharField(max_length=200, unique=True, verbose_name='Name')
    total_m = models.IntegerField(default=0, verbose_name='Gesamtdistanz in m')
    category = models.CharField(max_length=10, choices=CATEGORYS, default="GEMISCHT", verbose_name='Kategorie')

    def __str__(self):
        """
        Gibt das Objekt der Klasse als Text im Format 'T#1 - 2000m' zurück.
        :return: String
        """
        return f'{self.name} - {self.total_m}m'

class Task(models.Model):
    """
    Speichert eine Aufgabe in einem :model:`club.Trainingplan` mit Distanz, Wiederholungen, Teilstrecke und optionaler
    Intensität, Hilfsmittel und Kommentar.
    """
    swim_speeds = [
        ('loc', 'loc'),
        ('GA1', 'GA1'),
        ('GA2', 'GA2'),
        ('WSA', 'WSA'),
        ('sprint', 'sprint')
    ]

    training_plan = models.ForeignKey(
        Trainingplan, on_delete=models.CASCADE
    )
    total_distance = models.IntegerField(blank=True, null=True, verbose_name='Distanz in m')
    number_parts = models.IntegerField(default=1, verbose_name='Wiederholungen')
    part_distance = models.IntegerField(verbose_name='Teilstrecke in m')
    part_task = models.TextField(verbose_name='Aufgabe')
    intensiity = models.CharField(max_length= 100, choices=swim_speeds, blank=True, verbose_name='Intensität')
    tools = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hilfsmittel')
    comment = models.CharField(max_length=200, blank=True, null=True, verbose_name='Kommentar')


class Training(models.Model):
    """
    Speichert ein Training einer :model:`club.SwimmGroup` mit Startzeit, Endzeit, :model:`club.Trainer` und optionalem
    :model:`club.Trainingplan`.
    """
    group = models.ForeignKey(SwimmGroup, on_delete=models.CASCADE, related_name='swimm_group', verbose_name='Schwimmgruppe')
    start_time = models.DateTimeField(verbose_name='Startzeit')
    end_time = models.DateTimeField(verbose_name='Endzeit')
    training_plan = models.ForeignKey(
        Trainingplan, on_delete=models.CASCADE, verbose_name='Trainingsplan', blank=True, null=True
    )
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, verbose_name='Trainer', )

    @property
    def get_html_url(self):
        """
        Gibt einen HTML Element mit URL für die Detailseite des Trainings zurück.
        :return: String
        """
        url = reverse('training-detail', args=(self.id,))
        return f'<a href="{url}"> {self.group.short_name} {self.start_time.strftime("%H:%M")}-{self.end_time.strftime("%H:%M")} </a>'

    def __str__(self):
        """
        Gibt das Objekt der Klasse als Text im Format '01.01 2023 19:00' zurück.
        :return: String
        """
        return f'{self.start_time.strftime("%d.%m %Y %H:%M")}'

    def get_absolute_url(self):
        """
        Gibt die URL für die Detailseite des Trainings zurück.
        :return: url
        """
        return reverse('training-detail', args=[str(self.id)])

class Attendance(models.Model):
    """
    Speichert die Anwesentheit eines :model:`club.Swimmer` zu einem :model:`club.Training` mit einem Status.
    """
    STATES = [
        ("ANWESEND", "a"),
        ("ENTSCHULDIGT", "e"),
        ("UNENTSCHULDIGT", "u"),
        ("UNBEKANNT", "x")
    ]
    training = models.ForeignKey(Training, on_delete=models.CASCADE,  verbose_name='Training')
    swimmer = models.ForeignKey(Swimmer, on_delete=models.CASCADE, verbose_name='Schwimmer')
    status = models.CharField(max_length=20, choices=STATES, default="UNBEKANNT", verbose_name='Anwesenheit')