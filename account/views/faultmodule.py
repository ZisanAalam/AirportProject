from account.models import FaultLocationPart
from account.forms import FaultModuleForm
from django.contrib import messages
from account.decorators import unauthenticated_user
from django.shortcuts import render,redirect

@unauthenticated_user
def view_faultmodule(request):
    faultmodule  = FaultLocationPart.objects.all()
    return render(request,'faultmodule/viewfaultmodule.html',{'faultmodules':faultmodule})

@unauthenticated_user
def add_faultmodule(request):
    if request.method=="POST":
        fm = FaultModuleForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Fault Module Added Successfully !!! ')
            fm.save()
            return redirect('viewfaultmodule')
    else: 
        fm = FaultModuleForm
    return render(request, 'faultmodule/addfaultmodule.html',{'form':fm})

@unauthenticated_user
def edit_faultmodule(request,id):
    if request.method=='POST':
        pi = FaultLocationPart.objects.get(pk=id)
        fm = FaultModuleForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(
                request, "Fault Module Updated Successfully !!!")
            return redirect('viewfaultmodule')
    else:
        pi = FaultLocationPart.objects.get(pk=id)
        fm = FaultModuleForm(instance=pi)
    return render(request, 'faultmodule/editfaultmodule.html',{'form':fm})

@unauthenticated_user
def delete_faultmodule(request,id):
    fm = FaultLocationPart.objects.get(pk=id)
    if request.method=='POST':
        pi = FaultLocationPart.objects.get(pk=id)
        pi.delete()
        messages.success(request, 'Fault Module Deleted Successfully !!! ')
        return redirect('viewfaultmodule')
    return render(request, 'faultmodule/delete_confirm.html',{'faultmodule':fm.name})