from account.models import Make
from account.forms import MakeForm
from django.shortcuts import render,redirect
from django.contrib import messages
from account.decorators import unauthenticated_user

@unauthenticated_user
def view_make(request):
    makes =  Make.objects.all()
    return render(request,'make/viewmake.html',{'makes':makes})

@unauthenticated_user
def add_make(request):
    if request.method=="POST":
        fm = MakeForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Make Added Successfully !!! ')
            fm.save()
            return redirect('viewmake')
    else: 
        fm = MakeForm
    return render(request, 'make/addmake.html',{'form':fm})

@unauthenticated_user
def edit_make(request,id):
    if request.method=='POST':
        pi = Make.objects.get(pk=id)
        fm = MakeForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(
                request, "Make Updated Successfully !!!")
            return redirect('viewmake')
    else:
        pi = Make.objects.get(pk=id)
        fm = MakeForm(instance=pi)
    return render(request, 'make/editmake.html',{'form':fm})

@unauthenticated_user
def delete_make(request,id):
    make = Make.objects.get(pk=id)
    if request.method=='POST':
        pi = Make.objects.get(pk=id)
        pi.delete()
        messages.success(request, 'Make Deleted Successfully !!! ')
        return redirect('viewmake')
    return render(request, 'make/delete_confirm.html',{'make_name':make.name})