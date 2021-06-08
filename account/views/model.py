from account.models import Model
from account.forms import ModelForm
from django.shortcuts import render,redirect
from django.contrib import messages
from account.decorators import unauthenticated_user

@unauthenticated_user
def view_model(request):
    models =  Model.objects.all()
    return render(request,'model/viewmodel.html',{'models':models})

@unauthenticated_user
def add_model(request):
    if request.method=="POST":
        fm = ModelForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Model Added Successfully !!! ')
            fm.save()
            return redirect('viewmodel')
    else: 
        fm = ModelForm
    return render(request, 'model/addmodel.html',{'form':fm})

@unauthenticated_user
def edit_model(request,id):
    if request.method=='POST':
        pi = Model.objects.get(pk=id)
        fm = ModelForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(
                request, "Model Updated Successfully !!!")
            return redirect('viewmodel')
    else:
        pi = Model.objects.get(pk=id)
        fm = ModelForm(instance=pi)
    return render(request, 'model/editmodel.html',{'form':fm})

@unauthenticated_user
def delete_model(request,id):
    model = Model.objects.get(pk=id)
    if request.method=='POST':
        pi = Model.objects.get(pk=id)
        pi.delete()
        messages.success(request, 'Model Deleted Successfully !!! ')
        return redirect('viewmodel')
    return render(request, 'model/delete_confirm.html',{'model_name':model.name})