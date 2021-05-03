from account.decorators import unauthenticated_user
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
@unauthenticated_user
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")