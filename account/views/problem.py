from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.db.models import F
from account.models import Equipment, Runway, FaultLocation, FaultEntry, FaultLocationPart, Model, Make
from account.decorators import unauthenticated_user
from account.forms import FaultEntryForm
from datetime import datetime, date
from .calc import gethours
from operator import itemgetter
import math


class ViewFault(TemplateView):
    template_name = 'navparameter/viewfault.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fm = FaultEntryForm()

        data = FaultEntry.objects.filter(
            runway__in=Runway.objects.filter(airport=self.request.user.airport))
        runways = Runway.objects.filter(airport=self.request.user.airport)
        equipments = Equipment.objects.filter(
            runway__airport=self.request.user.airport)
        make = Make.objects.all()
        model = Model.objects.all()
        locations = FaultLocation.objects.all()
        locationpart = FaultLocationPart.objects.all()
        context = {'form': fm, 'fault': data, 'equipments': equipments, 'make': make, 'model': model,
                   'runways': runways, 'locations': locations, 'locationpart': locationpart}
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
                   'runways': runways, 'locations': locations, 'makes': makes}
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

        dt = gethours.get_hrs(start_date_input, end_date_input,
                              start_time_input, end_time_input)
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
            make=make_obj,
            model=model_obj,
            date=start_date_input,
            period='2020-2020',
            down_time=down_time,
            location=location_obj,
            locationpart=locationpart_obj,
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
def get_location_parts(request, id):
    selected_location = id
    obj_models = list(FaultLocationPart.objects.filter(
        faultlocation_id=selected_location).values())
    return JsonResponse({'data': obj_models})


@unauthenticated_user
def get_model(request, id):
    selectedMake = id

    md = list(Model.objects.filter(make_id=selectedMake).values())

    return JsonResponse({'data': md})


@unauthenticated_user
def calculate_nav_parameter(request):
    makes = Make.objects.all()
    return render(request, 'navparameter/calculate_nav_parameters.html', {'makes': makes})


@unauthenticated_user
def nav_calculation(request):
    if request.method == "GET":

        # Retrieve GET Parameters
        makes_id = request.GET['makes']
        models_id = request.GET['models']
        start_date = request.GET['startdate']
        end_date = request.GET['enddate']

        # Check parameter validity
        if not makes_id or not models_id or not start_date or not end_date:
            return JsonResponse({'data': "invalid"})
        startdate = datetime.strptime(
            request.GET['startdate'], '%Y-%m-%d').date()
        enddate = datetime.strptime(request.GET['enddate'], '%Y-%m-%d').date()
        if (enddate-startdate).days*24 < 0:
            return JsonResponse({'data': "invalid"})

        # Retrieve fault entries corresponding to parameters provided
        fault_entries = FaultEntry.objects.filter(make__in=Make.objects.filter(
            pk=makes_id), model__in=Model.objects.filter(pk=models_id),
            date__gte=startdate, date__lte=enddate).order_by('equipment',
                                                             'location', 'locationpart').values(
            'id', 'equipment_id', 'down_time', 'location_id', 'locationpart_id')
        fault_entries = list(fault_entries)

        # Retrieve equipment,location and faulty module names
        for each_entry in fault_entries:
            each_entry['equipment'] = Equipment.objects.get(
                pk=each_entry['equipment_id']).equipment
            each_entry['location'] = FaultLocation.objects.get(
                pk=each_entry['location_id']).location
            each_entry['locationpart'] = FaultLocationPart.objects.get(
                pk=each_entry['locationpart_id']).name

        # Failure rate calculation for each module
        prev_item = (-1, -1, -1)
        recent_entry = {}
        items_to_be_removed = []
        for each_item in fault_entries:
            cur_item = (
                each_item['equipment_id'], each_item['location_id'], each_item['locationpart_id'])
            if cur_item == prev_item:
                recent_entry['num_failures'] += 1.0
                recent_entry['failure_time'] += float(each_item['down_time'])
                recent_entry['failure_rate'] = recent_entry['num_failures'] / \
                    recent_entry['failure_time']
                items_to_be_removed.append(each_item)
            else:
                recent_entry = each_item
                recent_entry['num_failures'] = 1.0
                recent_entry['failure_time'] = float(recent_entry['down_time'])
                recent_entry['operating_time'] = (enddate-startdate).days*24.0
                recent_entry['failure_rate'] = recent_entry['num_failures'] / \
                    recent_entry['failure_time']
            prev_item = cur_item

        # Remove redundant items with same equipment, location and faulty module as calculation already done for them
        for each_item_to_be_removed in items_to_be_removed:
            fault_entries.remove(each_item_to_be_removed)

        # Proceed calculation of nav parameter for each (equipment location combination)
        fault_entries.sort(key=itemgetter('location_id'))
        nav_parameters = []
        for index, each_item in enumerate(fault_entries):
            new_value = {}
            if index == 0:
                new_value = {
                    'total_failure_rate': each_item['failure_rate'],
                    'total_failure_time': each_item['failure_time'],
                    'operating_time': each_item['operating_time'],
                    'tx_mtbf': float('inf'),
                    'mx_mtbf': float('inf')
                }
                new_value['mtbo'] = 1.0/each_item['failure_rate']
            else:
                new_value = nav_parameters.pop()
                new_value['total_failure_rate'] += each_item['failure_rate']
                new_value['total_failure_time'] += each_item['failure_time']
                new_value['mtbo'] += 1.0/each_item['failure_rate']

            if each_item['location'] == 'TX':
                new_value['tx_mtbf'] = 1.0/each_item['failure_rate'] if new_value['tx_mtbf'] == float(
                    'inf') else (1.0/each_item['failure_rate'])+new_value['tx_mtbf']
            else:
                new_value['mx_mtbf'] = 1.0/each_item['failure_rate'] if new_value['mx_mtbf'] == float(
                    'inf') else (1.0/each_item['failure_rate'])+new_value['mx_mtbf']

            new_value['mtbf'] = 1.0/new_value['total_failure_rate']
            new_value['availability'] = (new_value['operating_time']-new_value['total_failure_time']) / \
                (new_value['operating_time'])
            new_value['integrity'] = 1.0 - \
                ((0.0334*0.0334) /
                 (0.5*0.5*new_value['tx_mtbf']*new_value['mx_mtbf']))
            new_value['reliability'] = math.exp(
                -24.0/(new_value['mtbo']*10**6))
            if each_item['equipment'] == 'GP':
                new_value['continuity'] = 1.0 - \
                    (15.0/(new_value['mtbo']*60.0*60.0))
            else:
                new_value['continuity'] = 1.0 - \
                    (30.0/(new_value['mtbo']*60.0*60.0))
            nav_parameters.append(new_value)
            if index == len(fault_entries) - 1:
                nav_parameters[0].pop('tx_mtbf')
                nav_parameters[0].pop('mx_mtbf')

        return JsonResponse({'data': fault_entries, 'navparams': nav_parameters})
