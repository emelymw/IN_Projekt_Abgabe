import calendar

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from .utils import Calendar
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, FormView, CreateView
from multi_form_view import MultiModelFormView
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.db import transaction
from datetime import date, datetime, timedelta
from django.contrib.auth.models import Group

#
# CLUB
#
class ClubUpdateFormView(MultiModelFormView):
    """
    Init FormView for ClubUpdate
    """
    template_name = "club/club_form.html"
    form_classes = {
        'club_form': ClubForm,
        'address_form': AddressForm,
    }

    def get_success_url(self):
        return reverse('club-detail')

    def forms_valid(self, forms):
        address = forms['address_form'].save()
        club = forms['club_form'].save(commit=False)
        club.address = address
        club.save()

        return super(ClubUpdateFormView, self).forms_valid(forms)

class ClubDetail(PermissionRequiredMixin, DetailView):
    """
    View for Detailpage of Club
    """
    permission_required = "club.view_club"
    model = Club

    def get_object(self, queryset=None):
        object = Club.objects.all().first()
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trainer_data'] = Trainer.objects.all()
        context['departmentManager_data'] = DepartmentManager.objects.all()
        return context

class ClubUpdate(PermissionRequiredMixin, UpdateView, ClubUpdateFormView):
    """
    View for Updatepage of Club
    """
    permission_required = "club.change_club"
    model = Club
    success_url = "/"

    def get_objects(self):
        club = Club.objects.all().first()
        return {
            'club_form': club,
            'address_form': club.address,
        }

#
# DEPARTMENTMANAGER
#
class DepartmentManagerCreateFormView(MultiModelFormView):
    """
    Init FormView for DepartmentManagerCreate
    """
    template_name = "club/departmentmanager_form.html"
    form_classes = {
        'user_form': UserCreateForm,
        'departmentManager_form': DepartmentManagerForm,
    }

    def get_success_url(self):
        return reverse('club-detail')

    def forms_valid(self, forms):
        user = forms['user_form'].save()
        departmentManager = forms['departmentManager_form'].save(commit=False)
        departmentManager.user = user
        departmentManager.save()
        my_group = Group.objects.get(name='departmentmanager group')
        my_group.user_set.add(user)
        my_group.save()

        return super(DepartmentManagerCreateFormView, self).forms_valid(forms)

class DepartmentManagerUpdateFormView(MultiModelFormView):
    """
    Init FormView for DepartmentManagerUpdate
    """
    template_name = "club/departmentmanager_updateform.html"
    form_classes = {
        'user_form': UserUpdateForm,
        'departmentManager_form': DepartmentManagerForm,
    }

    def get_success_url(self):
        return reverse('club-detail')

    def forms_valid(self, forms):
        user = forms['user_form'].save()
        departmentManager = forms['departmentManager_form'].save(commit=False)
        departmentManager.user = user
        departmentManager.save()

        return super(DepartmentManagerUpdateFormView, self).forms_valid(forms)

class DepartmentManagerCreate(PermissionRequiredMixin, CreateView, DepartmentManagerCreateFormView):
    """
    View for Createpage of DepartmentManager
    """
    permission_required = "club.add_departmentmanager"
    model = DepartmentManager

class DepartmentManagerDelete(PermissionRequiredMixin, DeleteView):
    """
    View for Deletepage of DepartmentManager
    """
    permission_required = "club.delete_departmentmanager"
    model = DepartmentManager
    success_url = reverse_lazy('club-detail')
    template_name = "club/confirm_delete.html"

    def get_object(self, queryset=None):
        user_found = User.objects.get(username=self.kwargs.get('username'))
        object = DepartmentManager.objects.get(user=user_found)
        return object

class DepartmentManagerUpdate(PermissionRequiredMixin,UpdateView, DepartmentManagerUpdateFormView):
    """
    View for Updatepage of DepartmentManager
    """
    permission_required = "club.change_departmentmanager"
    model = Trainer

    def get_objects(self):
        user_found = User.objects.get(username=self.kwargs.get('username'))
        departmentManager = DepartmentManager.objects.get(user=user_found)
        self.success_url = reverse_lazy('departmentmanger-detail', args=[user_found.username])
        return {
            'user_form': user_found,
            'departmentManager_form': departmentManager,
        }

#
# TRAINER
#
class TrainerCreateFormView(MultiModelFormView):
    """
    Init FormView for TrainerCreate
    """
    template_name = "club/trainer_form.html"
    form_classes = {
        'user_form': UserCreateForm,
        'trainer_form': TrainerForm,
    }

    def get_success_url(self):
        return reverse('club-detail')

    def forms_valid(self, forms):
        user = forms['user_form'].save()
        trainer = forms['trainer_form'].save(commit=False)
        trainer.user = user
        trainer.save()
        my_group = Group.objects.get(name='trainer group')
        my_group.user_set.add(user)
        my_group.save()

        return super(TrainerCreateFormView, self).forms_valid(forms)

class TrainerUpdateFormView(MultiModelFormView):
    """
    Init FormView for TrainerUpdate
    """
    template_name = "club/trainer_form.html"
    form_classes = {
        'user_form': UserUpdateForm,
        'trainer_form': TrainerForm,
    }

    def get_success_url(self):
        return reverse('club-detail')

    def forms_valid(self, forms):
        user = forms['user_form'].save()
        trainer = forms['trainer_form'].save(commit=False)
        trainer.user = user
        trainer.save()

        return super(TrainerUpdateFormView, self).forms_valid(forms)

class TrainerCreate(PermissionRequiredMixin, CreateView, TrainerCreateFormView):
    """
    View for Createpage of Trainer
    """
    permission_required = "club.add_trainer"
    model = Trainer

class TrainerDelete(PermissionRequiredMixin, DeleteView):
    """
    View for Deletepage of Trainer
    """
    permission_required = "club.delete_trainer"
    model = Trainer
    success_url = reverse_lazy('club-detail')
    template_name = "club/confirm_delete.html"

    def get_object(self, queryset=None):
        user_found = User.objects.get(username=self.kwargs.get('username'))
        object = Trainer.objects.get(user=user_found)
        return object

class TrainerDetail(PermissionRequiredMixin, DetailView):
    """
    View for Detailpage of Trainer
    """
    permission_required = "club.view_trainer"
    model = Trainer

    def get_object(self, queryset=None):
        user_found = User.objects.get(username=self.kwargs.get('username'))
        object = Trainer.objects.get(user=user_found)
        return object

class TrainerUpdate(PermissionRequiredMixin, UpdateView, TrainerUpdateFormView):
    """
    View for Detailpage of Trainer
    """
    permission_required = "club.change_trainer"
    model = Trainer

    def get_objects(self):
        user_found = User.objects.get(username=self.kwargs.get('username'))
        trainer = Trainer.objects.get(user=user_found)
        return {
            'user_form': user_found,
            'trainer_form': trainer,
        }

    def get_success_url(self):
        user_found = User.objects.get(username=self.kwargs.get('username'))
        return reverse('trainer-detail', kwargs={'username': user_found.username})

#
# SWIMMER
#
class SwimmerList(PermissionRequiredMixin, ListView):
    """
    View for Listpage of Swimmer
    """
    permission_required = "club.view_swimmer"
    paginate_by = 10
    model = Swimmer

class SwimmerDetail(PermissionRequiredMixin, DetailView):
    """
    View for Detailpage of Swimmer
    """
    permission_required = "club.view_swimmer"
    model = Swimmer

    def get_object(self, queryset=None):
        object = Swimmer.objects.get(dsv_id=self.kwargs.get('dsv_id'))
        return object

class SwimmerUpdate(PermissionRequiredMixin, UpdateView):
    """
    View for Updatepage of Swimmer
    """
    permission_required = "club.change_swimmer"
    form_class = SwimmerForm
    model = Swimmer

    def get_object(self, queryset=None):
        object = Swimmer.objects.get(dsv_id=self.kwargs.get('dsv_id'))
        self.success_url = reverse_lazy('swimmer-detail', args=[object.dsv_id])
        return object

class SwimmerCreate(PermissionRequiredMixin, CreateView):
    """
    View for Createpage of Swimmer
    """
    permission_required = "club.add_swimmer"
    form_class = SwimmerForm
    model = Swimmer

class SwimmerDelete(PermissionRequiredMixin, DeleteView):
    """
    View for Deletepage of Swimmer
    """
    permission_required = "club.delete_swimmer"
    model = Swimmer
    success_url = reverse_lazy('swimmer-list')
    template_name = "club/confirm_delete.html"

    def get_object(self, queryset=None):
        object = Swimmer.objects.get(dsv_id=self.kwargs.get('dsv_id'))
        return object

#
# TRAINING
#
class TrainingDetail(PermissionRequiredMixin, DetailView):
    """
    View for Detailpage of Training
    """
    permission_required = "club.view_training"
    model = Training

    def get_object(self, queryset=None):
        object = Training.objects.get(id=self.kwargs.get('id'))
        return object

class TrainingDelete(PermissionRequiredMixin, DeleteView):
    """
    View for Deletepage of Training
    """
    permission_required = "club.delete_training"
    model = Training
    success_url = reverse_lazy('training-calendar')
    template_name = "club/confirm_delete.html"

class TrainingTrainingplan(PermissionRequiredMixin, UpdateView):
    """
    View for UpdateTrainingplan of Training
    """
    permission_required = "club.change_training"
    model = Training
    fields = ['training_plan']

class TrainingTrainer(PermissionRequiredMixin, UpdateView):
    """
    View for UpdateTrainer of Training
    """
    permission_required = "club.change_training"
    model = Training
    fields = ['trainer']

class TrainingAttendanceCreate(PermissionRequiredMixin, FormView):
    """
    View for CreateAttendance of Training
    """
    permission_required = "club.add_attendance"
    template_name = "club/trainingattendance_form.html"
    form_class = TrainingAttendanceForm
    success_url = reverse_lazy('training-calendar')

    def get_initial(self):
        initial = super(TrainingAttendanceCreate, self).get_initial()
        initial.update({'training': self.request.resolver_match.kwargs["pk"]})
        return initial

    def form_valid(self, form):
        training = Training.objects.get(pk=self.kwargs['pk'])
        swimmers = form.cleaned_data
        for swimmer_name in swimmers:
            names = swimmer_name.split()
            swimmer = Swimmer.objects.get(dsv_id=names[2])
            Attendance.objects.create(training=training, swimmer=swimmer, status=swimmers[swimmer_name])

        return super(TrainingAttendanceCreate, self).form_valid(form)

    def get_success_url(self):
        training_found = Training.objects.get(id=self.kwargs.get('pk'))
        return reverse('training-detail', kwargs={'id': training_found.id})

class TrainingAttendanceUpdate(PermissionRequiredMixin, FormView):
    """
    View for UpdateAttendance of Training
    """
    permission_required = "club.change_attendance"
    template_name = "club/trainingattendance_form.html"
    form_class = TrainingAttendanceFormUpdate
    success_url = reverse_lazy('training-calendar')

    def get_initial(self):
        initial = super(TrainingAttendanceUpdate, self).get_initial()
        initial.update({'training': self.request.resolver_match.kwargs["pk"]})
        return initial

    def form_valid(self, form):
        training = Training.objects.get(pk=self.kwargs['pk'])
        swimmers = form.cleaned_data
        for swimmer_name in swimmers:
            names = swimmer_name.split()
            swimmer = Swimmer.objects.get(dsv_id=names[2])
            attendance = Attendance.objects.get(training=training, swimmer=swimmer)
            attendance.status = swimmers[swimmer_name]
            attendance.save()

        return super(TrainingAttendanceUpdate, self).form_valid(form)

    def get_success_url(self):
        training_found = Training.objects.get(id=self.kwargs.get('pk'))
        return reverse('training-detail', kwargs={'id': training_found.id})

#
# CALENDER
#
class CalendarView(PermissionRequiredMixin, ListView):
    """
    View for Calenderpage of Training
    """
    permission_required = "club.view_training"
    model = Training
    template_name = 'club/training_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

#
# SWIMMGROUP
#
class SwimmGroupCreate(PermissionRequiredMixin, CreateView):
    """
    View for Createpage of Swimmgroup
    """
    permission_required = "club.add_swimmgroup"
    form_class = SwimmGroupForm
    model = SwimmGroup
    success_url = reverse_lazy('swimmgroup-list')

    def get_context_data(self, **kwargs):
        data = super(SwimmGroupCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['trainingsdays'] = TrainingsDayFormSet(self.request.POST)
        else:
            data['trainingsdays'] = TrainingsDayFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        trainingsdays = context['trainingsdays']
        with transaction.atomic():
            self.object = form.save()

            if trainingsdays.is_valid():
                trainingsdays.instance = self.object
                trainingsdays.save()

                for trainingsday in trainingsdays.cleaned_data:
                    start_time = trainingsday['start_time']
                    end_time = trainingsday['end_time']
                    start_date = trainingsday['date']
                    start_datetime = datetime.combine(start_date, start_time)
                    end_datetime = datetime.combine(start_date, end_time)
                    for i in range(52):
                        Training.objects.create(group=self.object, start_time=start_datetime, end_time=end_datetime)
                        start_datetime = start_datetime + timedelta(days=7)
                        end_datetime = end_datetime + timedelta(days=7)


        return super(SwimmGroupCreate, self).form_valid(form)

class SwimmGroupUpdate(PermissionRequiredMixin, UpdateView):
    """
    View for Updatepage of Swimmgroup
    """
    permission_required = "club.change_swimmgroup"
    form_class = SwimmGroupForm
    model = SwimmGroup
    success_url = reverse_lazy('swimmgroup-list')

    def get_context_data(self, **kwargs):
        data = super(SwimmGroupUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['trainingsdays'] = TrainingsDayFormSet(self.request.POST, instance=self.object)
        else:
            data['trainingsdays'] = TrainingsDayFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        trainingsdays = context['trainingsdays']
        with transaction.atomic():
            self.object = form.save()

            if trainingsdays.is_valid():
                trainingsdays.instance = self.object
                trainingsdays.save()

        return super(SwimmGroupUpdate, self).form_valid(form)

    def get_success_url(self):
        swimmgroup_found = SwimmGroup.objects.get(id=self.kwargs.get('pk'))
        return reverse('swimmgroup-detail', kwargs={'id': swimmgroup_found.id})

class SwimmGroupList(PermissionRequiredMixin, ListView):
    """
    View for Listpage of Swimmgroup
    """
    permission_required = "club.view_swimmgroup"
    model = SwimmGroup

class SwimmGroupDetail(PermissionRequiredMixin, DetailView):
    """
    View for Detailpage of Swimmgroup
    """
    permission_required = "club.view_swimmgroup"
    model = SwimmGroup

    def get_object(self, queryset=None):
        object = SwimmGroup.objects.get(id=self.kwargs.get('id'))
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['swimmer_data'] = Swimmer.objects.filter(group=context['object'])
        context['trainings_days'] = TrainingsDay.objects.filter(swimm_group=context['object'])
        return context

class SwimmGroupDelete(PermissionRequiredMixin, DeleteView):
    """
    View for Deletepage of Swimmgroup
    """
    permission_required = "club.delete_swimmgroup"
    model = SwimmGroup
    success_url = reverse_lazy('swimmgroup-list')
    template_name = "club/confirm_delete.html"

    def get_object(self, queryset=None):
        object = SwimmGroup.objects.get(id=self.kwargs.get('id'))
        return object

#
# TRAININGPLAN
#
class TrainingsplanList(PermissionRequiredMixin, ListView):
    """
    View for Listpage of Trainingplan
    """
    permission_required = "club.view_trainingplan"
    paginate_by = 10
    model = Trainingplan

class TrainingsplanDetail(PermissionRequiredMixin, DetailView):
    """
    View for Detailpage of Trainingplan
    """
    permission_required = "club.view_trainingplan"
    model = Trainingplan

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(training_plan=context['object'])
        return context

class TrainingsplanCreate(PermissionRequiredMixin, CreateView):
    """
    View for Createpage of Trainingplan
    """
    permission_required = "club.add_trainingplan"
    model = Trainingplan
    fields = '__all__'
    success_url = reverse_lazy('trainingplan-list')

    def get_context_data(self, **kwargs):
        data = super(TrainingsplanCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['tasks'] = TaskFormSet(self.request.POST)
        else:
            data['tasks'] = TaskFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tasks = context['tasks']
        with transaction.atomic():
            self.object = form.save()

            if tasks.is_valid():
                tasks.instance = self.object
                tasks.save()
        return super(TrainingsplanCreate, self).form_valid(form)

class TrainingsplanUpdate(PermissionRequiredMixin, UpdateView):
    """
    View for Updatepage of Trainingplan
    """
    permission_required = "club.change_trainingplan"
    model = Trainingplan
    fields = '__all__'
    success_url = reverse_lazy('trainingplan-list')

    def get_context_data(self, **kwargs):
        data = super(TrainingsplanUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['tasks'] = TaskFormSet(self.request.POST, instance=self.object)
        else:
            data['tasks'] = TaskFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tasks = context['tasks']
        with transaction.atomic():
            self.object = form.save()

            if tasks.is_valid():
                tasks.instance = self.object
                tasks.save()
        return super(TrainingsplanUpdate, self).form_valid(form)

class TrainingsplanDelete(PermissionRequiredMixin, DeleteView):
    """
    View for Deletepage of Trainingplan
    """
    permission_required = "club.delete_trainingplan"
    model = Trainingplan
    success_url = reverse_lazy('trainingplan-list')
    template_name = "club/confirm_delete.html"