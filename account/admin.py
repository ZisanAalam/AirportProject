from django.contrib import admin
from .models import Profile, Runway, Equipment,FaultEntry, FaultLocation

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'image','user_id']

admin.site.register(Runway)
admin.site.register(Equipment)

@admin.register(FaultEntry)
class FaultEntryAdmin(admin.ModelAdmin):
    list_display = ['equipment','runway','start_date','end_date','start_time','end_time','fault_discription','action_taken']

@admin.register(FaultLocation)
class FaultLocationAdmin(admin.ModelAdmin):
    list_display = ['location']


admin.site.site_header = "Airport Authority of India"