from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Runway, Equipment, FaultEntry, FaultLocation, Airport, MyUser, FaultLocationPart,Make,Model

# Register your models here.


class UserAdmin(BaseUserAdmin):
    ordering = ('user_name',)
    search_fields = ('email', 'user_name', 'first_name',
                     'middle_name', 'last_name', 'phone', 'address',)
    list_filter = ('is_active', 'is_staff', 'groups',)
    list_display = ('user_name', 'email', 'first_name',
                    'is_active', 'is_staff', )
    fieldsets = (
        ('Account', {'fields': ('email', 'user_name', 'password',), },),
        ('Personal', {'fields': (('first_name',
         'middle_name',), 'last_name', 'phone', 'address',)}),
        ('Airport', {'fields': ('airport',)}),
        ('Permissions', {'fields': ('is_staff',
         'is_active'), 'description': 'Check the "is staff" option to provide admin access and check the "is active" option to verify users'},
         ),
        ('Groups', {'fields': ('groups',)}),
        ('Image', {'fields': ('image',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2', 'airport', 'is_active', 'is_staff', 'groups',)}
         ),
    )

    def get_queryset(self, request):
        all_users = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return all_users
        all_users = all_users.exclude(
            id__in=[each_user.id for each_user in all_users if each_user.is_superuser])
        return all_users.filter(airport=request.user.airport)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "airport" and not request.user.is_superuser:
            kwargs["queryset"] = Airport.objects.filter(
                id=request.user.airport.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(MyUser, UserAdmin)


class RunwayAdmin(admin.ModelAdmin):
    list_display = ('runway', 'airport')

    def get_queryset(self, request):
        all_runways = super(RunwayAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return all_runways
        return all_runways.filter(airport=request.user.airport)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "airport" and not request.user.is_superuser:
            kwargs["queryset"] = Airport.objects.filter(
                id=request.user.airport.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Runway, RunwayAdmin)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display =['id','equipment','runway']

admin.site.register(Airport)
admin.site.register(FaultLocationPart)
admin.site.register(Make)
admin.site.register(Model)


@admin.register(FaultEntry)
class FaultEntryAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'runway', 'date', 'period',
                    'down_time', 'fault_discription', 'action_taken']

    def get_queryset(self, request):
        all_faultentries = super(
            FaultEntryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return all_faultentries
        return all_faultentries.filter(runway__in=Runway.objects.filter(airport=request.user.airport))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "runway" and not request.user.is_superuser:
            kwargs["queryset"] = Runway.objects.filter(
                airport=request.user.airport)
        elif db_field.name == "location" and not request.user.is_superuser:
            kwargs["queryset"] = FaultLocation.objects.filter(
                airport=request.user.airport)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(FaultLocation)
class FaultLocationAdmin(admin.ModelAdmin):
    list_display = ['location', 'airport']

    def get_queryset(self, request):
        all_faultlocations = super(
            FaultLocationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return all_faultlocations
        return all_faultlocations.filter(airport=request.user.airport)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "airport" and not request.user.is_superuser:
            kwargs["queryset"] = Airport.objects.filter(
                id=request.user.airport.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.site_header = "Airports Authority of India"
admin.site.index_title = "Admin site"
admin.site.site_title = "Airports Authority of India"
