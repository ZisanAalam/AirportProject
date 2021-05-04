from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.views.generic.base import  TemplateView
from account.models import Equipment,Runway,FaultLocation,FaultEntry,FaultLocationPart,Model,Make
from account.decorators import unauthenticated_user
from account.forms import FaultEntryForm
from .calc import gethours
class ViewFault(TemplateView):
    template_name = 'navparameter/viewfault.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fm = FaultEntryForm()
        
        data = FaultEntry.objects.filter(
            runway__in=Runway.objects.filter(airport=self.request.user.airport))
        runways = Runway.objects.filter(airport=self.request.user.airport)
        equipments = Equipment.objects.filter(runway__airport=self.request.user.airport)
        make = Make.objects.all()
        model = Model.objects.all()
        locations = FaultLocation.objects.all()
        locationpart = FaultLocationPart.objects.all()
        context = {'form': fm, 'fault': data, 'equipments': equipments, 'make':make,'model':model,
                   'runways': runways, 'locations': locations,'locationpart':locationpart}
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
        make_id = request.POST.get('make')
        model_id = request.POST.get('model')
        locationpart_id = request.POST.get('location-part')

        dt = gethours.get_hrs(start_date_input,end_date_input,start_time_input,end_time_input)
        down_time = "{0:.2f}".format(dt)
        equipment_obj = Equipment.objects.get(id=equipment_id)
        runway_obj = Runway.objects.get(id=runway_id)
        location_obj = FaultLocation.objects.get(id=location_id)
        locationpart_obj = FaultLocationPart.objects.get(id=locationpart_id)
        make_obj = Make.objects.get(id=make_id)
        model_obj = Model.objects.get(id=model_id)

        discription = request.POST.get("fault_discription")
        actiontaken = request.POST.get("action_taken")

        FaultEntry.objects.create(
            equipment=equipment_obj,
            runway=runway_obj,
            make = make_obj,
            model = model_obj,
            date=start_date_input,
            period = '2020-2020', 
            down_time = down_time,
            location=location_obj,
            locationpart = locationpart_obj,
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
def get_location_parts(request,id):
    selected_location = id
    obj_models = list(FaultLocationPart.objects.filter(faultlocation_id=selected_location).values())
    return JsonResponse({'data':obj_models})

@unauthenticated_user
def get_model(request,id):
    selectedMake = id

    md = list(Model.objects.filter(make_id = selectedMake).values())

    return JsonResponse({'data':md})

@unauthenticated_user
def calculate_nav_parameter(request):
    makes = Make.objects.all()
    return render(request, 'navparameter/calculate_nav_parameters.html',{'makes':makes})