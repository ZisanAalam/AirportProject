
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.views.generic.base import  TemplateView
from account.models import Equipment,Runway,FaultLocation,FaultEntry,FaultLocationPart,Model,Make
from account.decorators import unauthenticated_user
from account.forms import FaultEntryForm

class ViewFault(TemplateView):
    template_name = 'navparameter/viewfault.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fm = FaultEntryForm()
        
        data = FaultEntry.objects.filter(
            runway__in=Runway.objects.filter(airport=self.request.user.airport))
        runways = Runway.objects.filter(airport=self.request.user.airport)
        equipments = Equipment.objects.filter(runway__airport=self.request.user.airport)
        locations = FaultLocation.objects.all()

        context = {'form': fm, 'fault': data, 'equipments': equipments,
                   'runways': runways, 'locations': locations}
        return context

class AddFaultView(TemplateView):
    template_name = 'navparameter/addfault.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipments = Equipment.objects.all()
        
        runways = Runway.objects.filter(airport=self.request.user.airport)
        locations = FaultLocation.objects.filter(
            airport=self.request.user.airport)
        
        makes = Make.objects.all()
        context = {'equipments': equipments,
                   'runways': runways, 'locations': locations,'makes':makes}
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

@unauthenticated_user
def deletefault(request, id):
    if request.method == 'POST':
        pi = FaultEntry.objects.get(pk=id)
        pi.delete()
        return redirect('viewfault')

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
def calculate_nav_parameter(request):
    return render(request, 'navparameter/calculate_nav_parameters.html')

@unauthenticated_user
def get_location_parts(request,id):
    selected_location = id
    obj_models = list(FaultLocationPart.objects.filter(faultlocation_id=selected_location).values())
    return JsonResponse({'data':obj_models})

@unauthenticated_user
def get_model(request,*args, **kwargs):
    selectedMake = kwargs.get('make')

    md = list(Model.objects.filter(make__name = selectedMake).values())

    return JsonResponse({'data':md})