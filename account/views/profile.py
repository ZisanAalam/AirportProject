from account.decorators import unauthenticated_user
from django.contrib import messages
from django.shortcuts import redirect,render
from account.forms import EditUserForm

@unauthenticated_user
def user_profile(request):
    return render(request, 'account/profile.html', {'name': request.user.first_name})

@unauthenticated_user
def user_profile_add(request):

    if request.method == 'POST':
        u_fm = EditUserForm(request.POST)
        if u_fm.is_valid():
            u_fm.save()
            messages.success(
                request, "Profile Updated Successfully !!!")
            return redirect('login')
    else:
        u_fm = EditUserForm(instance=request.user)
    return render(request, 'account/addprofile.html', {'form': u_fm})

@unauthenticated_user
def user_profile_edit(request):
    
    if request.method == 'POST':
        u_fm = EditUserForm(request.POST, request.FILES,instance=request.user)
        if u_fm.is_valid():
            u_fm.save()
            messages.success(
                request, "Profile Updated Successfully !!!")
            return redirect('profile')
    else:
        u_fm = EditUserForm(instance=request.user)
    return render(request, 'account/editprofile.html', {'u_form': u_fm})