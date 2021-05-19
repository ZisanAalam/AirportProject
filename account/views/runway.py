from account.models import Runway
from account.forms import RunwayForm
from django.shortcuts import render,redirect
from django.contrib import messages

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
    run = Runway.objects.get(pk=id)
    if request.method=='POST':
        pi = Runway.objects.get(pk=id)
        pi.delete()
        messages.success(request, 'Runway Deleted Successfully !!! ')
        return redirect('viewrunway')
    return render(request, 'account/deleteconfirm/delete_confirm.html',{'runway':run.runway})