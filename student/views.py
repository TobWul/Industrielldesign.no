import datetime

from django.db import models
from django.db.models import F
from django.shortcuts import render
from django.utils import timezone

from events.models import Event
from projects.models import Project


def home(request):
    def add_years(years):
        d = datetime.date.today()
        try:
            return d.replace(year=d.year + years)
        except ValueError:
            return d + (datetime.date(d.year + years, 1, 1) - datetime.date(d.year, 1, 1))

    now = timezone.now()
    events = (Event.objects.annotate(
        relevance=models.Case(
            models.When(event_start_time__gte=now, then=1),
            models.When(event_start_time__lt=now, then=2),
            output_field=models.IntegerField(),
        )).annotate(
        timediff=models.Case(
            models.When(event_start_time__gte=now, then=F('event_start_time') - now),
            models.When(event_start_time__lt=now, then=now - F('event_start_time')),
            output_field=models.DurationField(),
        )).order_by('relevance', 'timediff'))

    context = {
        "events": events[0:4],
        'projects': Project.objects.all()[0:7]
    }
    return render(request, 'index.html', context)


# STUDENT
def student(request):
    return render(request, 'student/student.html')


def klassetur(request):
    return render(request, 'student/klassetur.html')


def utveksling(request):
    return render(request, 'student/utveksling.html')


def ny_student(request):
    return render(request, 'student/ny-student.html')


def terms(request):
    return render(request, 'terms-conditions.html', {})