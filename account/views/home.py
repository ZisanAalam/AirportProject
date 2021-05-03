from account.decorators import unauthenticated_user
from django.shortcuts import render

@unauthenticated_user
def home_page(request):
    return render(request, 'account/home.html')
