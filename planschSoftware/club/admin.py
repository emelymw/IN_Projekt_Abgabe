from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class TrainerInline(admin.StackedInline):
    model = Trainer
    can_delete = False
    verbose_name_plural = 'Trainer'

class DepartmentManagerInline(admin.StackedInline):
    model = DepartmentManager
    can_delete = False
    verbose_name_plural = 'Abteilungsleiter'

class UserAdmin(BaseUserAdmin):
    inlines = (TrainerInline, DepartmentManagerInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Address)
admin.site.register(Trainer)
admin.site.register(DepartmentManager)
admin.site.register(Club)

admin.site.register(TrainingsDay)
admin.site.register(SwimmGroup)
admin.site.register(Swimmer)

admin.site.register(Training)
admin.site.register(Attendance)
admin.site.register(Trainingplan)
admin.site.register(Task)