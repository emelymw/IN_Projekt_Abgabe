from django import template
from club.models import Swimmer, Attendance, Training
from django.utils.formats import date_format
from django.utils import translation
from datetime import date

register = template.Library()

@register.filter(name="group_swimmer_count")
def group_swimmer_count(value):
    return Swimmer.objects.filter(group=value).count()

@register.filter(name="get_username")
def get_username(form):
    return form.initial['username']

@register.filter(name='attendance_exits')
def attendance_exits(training_id):
    return Attendance.objects.filter(training=training_id)

@register.filter(name='get_attendance')
def get_attendance(training_id):
    return Attendance.objects.filter(training=training_id)

@register.filter(name='present')
def present(swimmer):
    count_a = Attendance.objects.filter(swimmer=swimmer, status='ANWESEND').count()
    count_e = Attendance.objects.filter(swimmer=swimmer, status='ENTSCHULDIGT').count()
    count_u = Attendance.objects.filter(swimmer=swimmer, status='UNENTSCHULDIGT').count()
    count_all = count_a + count_e + count_u
    if count_all == 0:
        return '-'
    return (count_a / count_all) * 100

@register.filter(name='excused')
def excused(swimmer):
    count_a = Attendance.objects.filter(swimmer=swimmer, status='ANWESEND').count()
    count_e = Attendance.objects.filter(swimmer=swimmer, status='ENTSCHULDIGT').count()
    count_u = Attendance.objects.filter(swimmer=swimmer, status='UNENTSCHULDIGT').count()
    count_all = count_a + count_e + count_u
    if count_all == 0:
        return '-'
    return (count_e / count_all) * 100

@register.filter(name='unapologetic')
def unapologetic(swimmer):
    count_a = Attendance.objects.filter(swimmer=swimmer, status='ANWESEND').count()
    count_e = Attendance.objects.filter(swimmer=swimmer, status='ENTSCHULDIGT').count()
    count_u = Attendance.objects.filter(swimmer=swimmer, status='UNENTSCHULDIGT').count()
    count_all = count_a + count_e + count_u
    if count_all == 0:
        return '-'
    return (count_u / count_all) * 100

@register.filter(name='own_date')
def own_date(date, format):
    translation.activate('de')
    return date_format(date, format)