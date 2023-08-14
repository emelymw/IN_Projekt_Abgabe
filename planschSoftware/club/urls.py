from django.urls import path, re_path, register_converter
from . import views
from .views import *
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='club-detail', permanent=False)),
    path('passwort_change/', auth_views.PasswordChangeView.as_view(template_name='club/change_password.html'), name='user-changepassword'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('club/', ClubDetail.as_view(), name='club-detail'),
    path('club/update', ClubUpdate.as_view(), name='club-update'),

    path('departmentmanager/create', DepartmentManagerCreate.as_view(), name='departmentmanger-create'),
    path('departmentmanager/<str:username>/update', DepartmentManagerUpdate.as_view(), name='departmentmanger-update'),
    path('departmentmanager/<str:username>/delete', DepartmentManagerDelete.as_view(), name='departmentmanger-delete'),

    path('trainer/create', TrainerCreate.as_view(), name='trainer-create'),
    path('trainer/<str:username>/', TrainerDetail.as_view(), name='trainer-detail'),
    path('trainer/<str:username>/update', TrainerUpdate.as_view(), name='trainer-update'),
    path('trainer/<str:username>/delete', TrainerDelete.as_view(), name='trainer-delete'),

    path('swimmgroup/', SwimmGroupList.as_view(), name='swimmgroup-list'),
    path('swimmgroup/create', SwimmGroupCreate.as_view(), name='swimmgroup-create'),
    path('swimmgroup/<int:id>/', SwimmGroupDetail.as_view(), name='swimmgroup-detail'),
    path('swimmgroup/<int:pk>/update', SwimmGroupUpdate.as_view(), name='swimmgroup-update'),
    path('swimmgroup/<int:id>/delete', SwimmGroupDelete.as_view(), name='swimmgroup-delete'),

    path('swimmer/', SwimmerList.as_view(), name='swimmer-list'),
    path('swimmer/create', SwimmerCreate.as_view(), name='swimmer-create'),
    path('swimmer/<str:dsv_id>/', SwimmerDetail.as_view(), name='swimmer-detail'),
    path('swimmer/<str:dsv_id>/update', SwimmerUpdate.as_view(), name='swimmer-update'),
    path('swimmer/<str:dsv_id>/delete', SwimmerDelete.as_view(), name='swimmer-delete'),

    path('training/', CalendarView.as_view(), name='training-calendar'),
    path('training/<int:id>/', TrainingDetail.as_view(), name='training-detail'),
    path('training/<int:pk>/delete', TrainingDelete.as_view(), name='training-delete'),
    path('training/<int:pk>/trainingplan', TrainingTrainingplan.as_view(), name='training-trainingplan'),
    path('training/<int:pk>/trainer', TrainingTrainer.as_view(), name='training-trainer'),
    path('training/<int:pk>/attendance/create', TrainingAttendanceCreate.as_view(), name='training-attendance-create'),
    path('training/<int:pk>/attendance/update', TrainingAttendanceUpdate.as_view(), name='training-attendance-update'),

    path('trainingplan/', TrainingsplanList.as_view(), name='trainingplan-list'),
    path('trainingplan/create', TrainingsplanCreate.as_view(), name='trainingplan-create'),
    path('trainingplan/<int:pk>/', TrainingsplanDetail.as_view(), name='trainingplan-detail'),
    path('trainingplan/<int:pk>/update', TrainingsplanUpdate.as_view(), name='trainingplan-update'),
    path('trainingplan/<int:pk>/delete', TrainingsplanDelete.as_view(), name='trainingplan-delete'),
]
