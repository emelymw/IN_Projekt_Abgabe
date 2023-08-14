from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.forms import inlineformset_factory

class UserCreateForm(UserCreationForm):
    """
    Form for UserCreate
    """
    first_name = forms.CharField(max_length=50, label='Vorname')  # Required
    last_name = forms.CharField(max_length=50, label='Nachname')  # Required
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    """
    Form for UserUpdate
    """
    first_name = forms.CharField(max_length=50, label='Vorname')  # Required
    last_name = forms.CharField(max_length=50, label='Nachname')  # Required
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class TrainerForm(forms.ModelForm):
    """
    Form for Trainer
    """
    class Meta:
        model = Trainer
        fields = ['birth_date', 'education', 'expiry_date_first_aid', 'expiry_date_lifeguard']
        widgets = {
            'birth_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'expiry_date_first_aid': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'expiry_date_lifeguard': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

class DepartmentManagerForm(forms.ModelForm):
    """
    Form for DepartmentManager
    """
    class Meta:
        model = DepartmentManager
        fields = ['email']

class AddressForm(forms.ModelForm):
    """
    Form for Address
    """
    class Meta:
        model = Address
        fields = "__all__"

class ClubForm(forms.ModelForm):
    """
    Form for Club
    """
    class Meta:
        model = Club
        fields = ['name', 'short_name', 'department']

class TrainingForm(forms.ModelForm):
    """
    Form for Training
    """
    class Meta:
        model = Training
        widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'start_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M'),
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M'),

class TrainingAttendanceForm(forms.ModelForm):
    """
    Form for AttendanceCreate
    """
    class Meta:
        model = Training
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        STATES = [
            ("UNBEKANNT", "x"),
            ("ANWESEND", "a"),
            ("ENTSCHULDIGT", "e"),
            ("UNENTSCHULDIGT", "u"),
        ]
        training = Training.objects.get(pk=kwargs["initial"]["training"])
        swimmers = Swimmer.objects.filter(group=training.group)
        for swimmer in swimmers:
            field_name = f'{swimmer.first_name} {swimmer.last_name} {swimmer.dsv_id}'
            self.fields[field_name] = forms.ChoiceField(choices=STATES)

class TrainingAttendanceFormUpdate(forms.ModelForm):
    """
    Form for AttendanceUpdate
    """
    class Meta:
        model = Training
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        STATES = [
            ("UNBEKANNT", "x (unbekannt)"),
            ("ANWESEND", "a (anwesend)"),
            ("ENTSCHULDIGT", "e (entschuldigt)"),
            ("UNENTSCHULDIGT", "u (unentschuldigt)"),
        ]
        training = Training.objects.get(pk=kwargs["initial"]["training"])
        swimmers = Swimmer.objects.filter(group=training.group)
        for swimmer in swimmers:
            field_name = f'{swimmer.first_name} {swimmer.last_name} {swimmer.dsv_id}'
            self.fields[field_name] = forms.ChoiceField(choices=STATES)
            attendance = Attendance.objects.get(training=training, swimmer=swimmer)
            self.fields[field_name].initial = attendance.status

class SwimmGroupForm(forms.ModelForm):
    """
    Form for SwimmGroup
    """
    class Meta:
        model = SwimmGroup
        fields = '__all__'
        widgets = {
            'trainer': forms.CheckboxSelectMultiple
        }

class SwimmerForm(forms.ModelForm):
    """
    Form for Swimmer
    """
    class Meta:
        model = Swimmer
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'attest': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

class TrainingsDaysForm(forms.ModelForm):
    """
    Form for TrainingsDay
    """
    class Meta:
        model = TrainingsDay
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'end_time': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }

TrainingsDayFormSet = inlineformset_factory(
    SwimmGroup, TrainingsDay, form=TrainingsDaysForm,
    extra=1, can_delete=True,
    can_delete_extra=True
)

class TrainingsplanForm(forms.ModelForm):
    """
    Form for Trainingplan
    """
    class Meta:
        model = Trainingplan
        fields = '__all__'

class TaskForm(forms.ModelForm):
    """
    Form for Task
    """
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'part_task': forms.Textarea(attrs={'rows': 4}),
        }

TaskFormSet = inlineformset_factory(
    Trainingplan, Task, form=TaskForm,
    extra=1, can_delete=True,
    can_delete_extra=True
)