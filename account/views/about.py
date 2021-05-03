from account.decorators import unauthenticated_user
from django.shortcuts import render

@unauthenticated_user
def About(request):
    return render(request, 'account/about.html')
