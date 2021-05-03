from django.contrib.auth import authenticate, login
from account.decorators import authenticated_user
from django.shortcuts import render, redirect
from account.forms import LoginForm
from django.contrib import messages

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
