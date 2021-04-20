from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Runway, Equipment, FaultEntry, FaultLocation, State, Airport

# Register your models here.


""" @admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'image', 'user_id')
    readonly_fields = ['user']

    def get_queryset(self, request):
        all_profiles = super(ProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return all_profiles
        profile_of_request_user = all_profiles.filter(user=request.user)
        return all_profiles.filter(airport=profile_of_request_user[0].airport)
 """

""" admin.site.unregister(User)


class UserAdmin(BaseUserAdmin):
    search_fields = ['username', 'first_name', 'last_name']
    list_display = ['username', 'first_name', 'is_active', 'is_staff']

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            self.fieldsets = (
                (None, {'fields': ('username', 'password',)}),
                ('Permissions', {'fields': ('is_staff', 'is_active')}),
                ('Groups', {'fields': ('groups',)})
            )
            self.add_fieldsets = (
                (None,
                 {
                     'classes': ('wide',),
                     'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff',)
                 }),
            )
        return super(UserAdmin, self).changelist_view(request, extra_context)

    def get_queryset(self, request):
        all_users = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return all_users
        all_users = all_users.exclude(
            id__in=[each_user.id for each_user in all_users if each_user.is_superuser])
        profile_of_current_user = Profile.objects.filter(user=request.user)
        state_of_user = profile_of_current_user[0].airport.state
        airport_of_user = profile_of_current_user[0].airport
        if request.user.groups.filter(name="State admin").exists():
            return all_users.filter(profile__in=Profile.objects.filter(airport__in=Airport.objects.filter(state=state_of_user)))
        all_users = all_users.exclude(
            id__in=[each_user.id for each_user in all_users if each_user.groups.filter(name="State admin").exists()])
        return all_users.filter(profile__in=Profile.objects.filter(airport=airport_of_user))


admin.site.register(User, UserAdmin) """

admin.site.register(Runway)
admin.site.register(Equipment)
admin.site.register(Airport)
admin.site.register(State)


@admin.register(FaultEntry)
class FaultEntryAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'runway', 'start_date', 'end_date',
                    'start_time', 'end_time', 'fault_discription', 'action_taken']


@admin.register(FaultLocation)
class FaultLocationAdmin(admin.ModelAdmin):
    list_display = ['location']


admin.site.site_header = "Airport Authority of India"


class AirportProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('airport',)

    def get_queryset(self, request):
        all_profiles = super(AirportProfileAdmin, self).get_queryset(request)
        profile_of_request_user = all_profiles.filter(user=request.user)
        return all_profiles.filter(airport=profile_of_request_user[0].airport)
