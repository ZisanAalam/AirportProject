from account.forms import CreateUserForm
from django.contrib import messages
from django.shortcuts import redirect,render
from account.models import MyUser

def user_signup(request):
    if request.method == "POST":
        fm = CreateUserForm(request.POST)
        if fm.is_valid():
            airport = fm.cleaned_data['airport']
            airport_admin = MyUser.objects.filter(is_staff=True, airport=airport)
            
            super_admin = MyUser.objects.filter(is_superuser=True)
            fm.save()
            messages.success(request, 'Account Created Successfully !!! ')
            return render(request, 'account/account_activate.html',{'airport_admin':airport_admin,'super_admin':super_admin})
    else:
        fm = CreateUserForm()
    return render(request, 'account/signup.html', {'form': fm})
