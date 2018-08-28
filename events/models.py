from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
import datetime

class Event(models.Model):
    NOW = datetime.datetime.now()
    YEAR = NOW.year
    if NOW.month > 7:
        YEAR += 1

    YEAR_CHOICES = [
        (YEAR+4, '1.klasse'),
        (YEAR+3, '2.klasse'),
        (YEAR+2, '3.klasse'),
        (YEAR+1, '4.klasse'),
        (YEAR, '5.klasse')
    ]
    def get_class_year(self, graduation_year):
        return graduation_year - self.YEAR

    title = models.CharField(max_length=80, unique=True)
    description = models.TextField()

    location = models.CharField(max_length=50, blank=True, null=True)
    open_for = models.CharField(max_length=50, blank=True, null=True)
    image = ProcessedImageField(upload_to='wiki/',processors=[ResizeToFit(2000, 2000, False)], format='JPEG', options={'quality': 85})
    

    # Event start
    event_start_time = models.DateTimeField()
    event_end_time = models.DateTimeField(blank=True, null=True)

    # Registration opens
    registration_required = models.BooleanField(default=False)
    registration_start_time = models.DateTimeField(blank=True, null=True)
    registration_year_limit = models.IntegerField('Åpent for n.klasse og opp', choices=YEAR_CHOICES, blank=True, null=True)

    # Available spots in the event
    available_spots = models.IntegerField(blank=True, null=True)
    

    registered_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    
    slug = models.SlugField(max_length=60, blank=True)

    # Event header image:
    # image = models.ImageField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            #Only set the slug when the object is created.
            self.slug = slugify(self.title) #Or whatever you want the slug to use
        super(Event, self).save(*args, **kwargs)

    class Meta:
        # ordering = ['event_start_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'