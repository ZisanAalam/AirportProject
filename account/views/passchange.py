from account.decorators import unauthenticated_user
from django.shortcuts import render
from account.forms import UserChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect

@unauthenticated_user
def user_change_pass(request):

    if request.method == 'POST':
        fm = UserChangePasswordForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            messages.success(request, "Password Changed Successfully !!!")
            return redirect('home')

    else:
        fm = UserChangePasswordForm(user=request.user)
    return render(request=request, template_name="account/changepassword/passworchange.html", context={"form": fm, 'name': request.user.first_name})
