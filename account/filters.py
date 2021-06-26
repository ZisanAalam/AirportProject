from django.db import models
import django_filters
from django_filters import DateFilter

from . models import  FaultEntry

class FaultEntryFilter(django_filters.FilterSet):
    start_date = DateFilter(label='From date', field_name='date',lookup_expr='gte')
    end_date = DateFilter(label='To date',field_name='date',lookup_expr='lte')
    #class Meta:
    #    model = FaultEntry
    #    fields = ['runway','equipment','make','model']