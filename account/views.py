from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import CreateUserForm, LoginForm, EditUserForm,  UserChangePasswordForm, FaultEntryForm, RunwayForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from .models import Airport, Equipment, MyUser, Runway, FaultEntry, FaultLocation
from django.views import View
from django.views.generic.base import RedirectView, TemplateView
from .decorators import authenticated_user, unauthenticated_user

# Create your views here.

@unauthenticated_user
def home(request):
    return render(request, 'account/home.html')


# About
@unauthenticated_user
def About(request):
    return render(request, 'account/about.html')


# Contact
@unauthenticated_user
def Contact(request):
    return render(request, 'account/contact.html')


# user profile
@unauthenticated_user
def user_profile(request):
    return render(request, 'account/profile.html', {'name': request.user.first_name})


# User Signup
def user_signup(request):
    if request.method == "POST":
        fm = CreateUserForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account Created Successfully !!! ')
            fm.save()
            return redirect('login')
    else:
        fm = CreateUserForm()
    return render(request, 'account/signup.html', {'form': fm})

# User Login


@authenticated_user
def user_login(request):
    if request.method == "POST":
        fm = LoginForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(user_name=uname, password=upass)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have logged in successfully')
                return redirect('home')
    else:
        fm = LoginForm()
    return render(request, 'account/login.html', {'form': fm})

# Logout


@unauthenticated_user
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")


# Change Password
@unauthenticated_user
def user_change_pass(request):

    if request.method == 'POST':
        fm = UserChangePasswordForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            messages.success(request, "Password Changed Successfully !!!")
            return redirect('home')

    else:
        fm = UserChangePasswordForm(user=request.user)
    return render(request=request, template_name="account/passworchange.html", context={"form": fm, 'name': request.user.first_name})

# update user profile


@unauthenticated_user
def user_profile_add(request):

    if request.method == 'POST':
        u_fm = EditUserForm(request.POST)
        if u_fm.is_valid():
            u_fm.save()
            messages.success(
                request, "Profile Updated Successfully Successfully !!!")
            return redirect('login')
    else:
        u_fm = EditUserForm(instance=request.user)
    return render(request, 'account/addprofile.html', {'form': u_fm})


# update user profile
@unauthenticated_user
def user_profile_edit(request):
    
    if request.method == 'POST':
        u_fm = EditUserForm(request.POST, instance=request.user)
        if u_fm.is_valid():
            u_fm.save()
            messages.success(
                request, "Profile Updated Successfully Successfully !!!")
            return redirect('profile')
    else:
        u_fm = EditUserForm(instance=request.user)
    return render(request, 'account/editprofile.html', {'u_form': u_fm})


class AddFaultView(TemplateView):
    template_name = 'navparameter/addfault.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipments = Equipment.objects.all()
        if not self.request.user.is_superuser:
            runways = Runway.objects.filter(airport=self.request.user.airport)
            locations = FaultLocation.objects.filter(
                airport=self.request.user.airport)
        else:
            runways = Runway.objects.all()
            locations = FaultLocation.objects.all()
        context = {'equipments': equipments,
                   'runways': runways, 'locations': locations}
        return context

    def post(self, request):
        equipment_id = request.POST.get("equipment")
        runway_id = request.POST.get("runway")
        start_date_input = request.POST.get("startdateinput")
        end_date_input = request.POST.get("endtdateinput")
        start_time_input = request.POST.get("starttimeinput")
        end_time_input = request.POST.get("endttimeinput")
        location_id = request.POST.get("location")

        equipment_obj = Equipment.objects.get(id=equipment_id)
        runway_obj = Runway.objects.get(id=runway_id)

        location_obj = FaultLocation.objects.get(id=location_id)

        discription = request.POST.get("fault_discription")
        actiontaken = request.POST.get("action_taken")

        FaultEntry.objects.create(
            equipment=equipment_obj,
            runway=runway_obj,
            start_date=start_date_input,
            end_date=end_date_input,
            start_time=start_time_input,
            end_time=end_time_input,
            location=location_obj,
            fault_discription=discription,
            action_taken=actiontaken

        )
        return redirect('viewfault')

# Add Fault


@unauthenticated_user
def updatefault(request, id):
    if request.method == 'POST':
        pi = FaultEntry.objects.get(pk=id)
        fm = FaultEntryForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            return redirect('viewfault')
    else:
        pi = FaultEntry.objects.get(pk=id)
        fm = FaultEntryForm(instance=pi, user=request.user)
        return render(request, 'navparameter/updatefault.html', {'form': fm})


@unauthenticated_user
def deletefault(request, id):
    if request.method == 'POST':
        pi = FaultEntry.objects.get(pk=id)
        pi.delete()
        return redirect('viewfault')


class ViewFault(TemplateView):
    template_name = 'navparameter/viewfault.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fm = FaultEntryForm()
        if not self.request.user.is_superuser:
            data = FaultEntry.objects.filter(
                runway__in=Runway.objects.filter(airport=self.request.user.airport))
            equipments = Equipment.objects.all()
            runways = Runway.objects.filter(airport=self.request.user.airport)
            locations = FaultLocation.objects.filter(
                airport=self.request.user.airport)
        else:
            data = FaultEntry.objects.all()
            equipments = Equipment.objects.all()
            runways = Runway.objects.all()
            locations = FaultLocation.objects.all()

        context = {'form': fm, 'fault': data, 'equipments': equipments,
                   'runways': runways, 'locations': locations}
        return context

# Calculate Navigation Parameter

@unauthenticated_user
def calculate_nav_parameter(request):
    return render(request, 'navparameter/calculate_nav_parameters.html')


#Runway
def view_runway(request):
    runways = Runway.runways = Runway.objects.filter(airport=request.user.airport)
    return render(request,'runway/viewrunway.html',{'runways':runways})

def add_runway(request):
    if request.method=="POST":
        fm = RunwayForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Runway Added Successfully !!! ')
            runway = fm.cleaned_data['runway']
            airport = request.user.airport
            Runway.objects.create(airport=airport,runway=runway)
            return redirect('viewrunway')
    else: 
        fm = RunwayForm
    return render(request, 'runway/addrunway.html',{'form':fm})

def edit_runway(request,id):
    if request.method=='POST':
        pi = Runway.objects.get(pk=id)
        fm = RunwayForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(
                request, "Runway Updated Successfully !!!")
            return redirect('viewrunway')
    else:
        pi = Runway.objects.get(pk=id)
        fm = RunwayForm(instance=pi)
    return render(request, 'runway/editrunway.html',{'form':fm})

def delete_runway(request,id):
    if request.method=='POST':
        pi = Runway.objects.get(pk=id)
        pi.delete()
        return redirect('viewrunway')