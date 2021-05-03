from account.forms import CreateUserForm
from django.contrib import messages
from django.shortcuts import redirect,render
def user_signup(request):
    if request.method == "POST":
        fm = CreateUserForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account Created Successfully !!! ')
            fm.save()
            return redirect('login')
    else:
        fm = CreateUserForm()
    return render(request, 'account/signup.html', {'form': fm})
