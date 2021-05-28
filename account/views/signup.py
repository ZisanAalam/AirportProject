from account.forms import CreateUserForm
from django.contrib import messages
from django.shortcuts import redirect,render
from account.models import MyUser
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse

def user_signup(request):
    if request.method == "POST":
        fm = CreateUserForm(request.POST)
        if fm.is_valid():
            airport = fm.cleaned_data['airport']
            first_name = fm.cleaned_data['first_name']
            email = fm.cleaned_data['email'].strip()
            airport_admin = MyUser.objects.filter(is_staff=True, airport=airport)
            
            super_admin = MyUser.objects.filter(is_superuser=True)
            
            temp = render_to_string('account/signup/account_activate_msg.html',{'airport_admin':airport_admin,'super_admin':super_admin,'name':first_name})
            try:
                email_to_send = EmailMessage(
                'Activate Your Account',
                temp,
                settings.EMAIL_HOST_USER,
                [email]
                )
                email_to_send.fail_silently = False
                email_to_send.send()
            
            except Exception as e:
                return HttpResponse('Error!!  Failed to send Email. Please check your internet connection and try again')
            

            fm.save()
            messages.success(request, 'Account Created Successfully !!! ')
            return render(request, 'account/signup/account_activate.html',{'airport_admin':airport_admin,'super_admin':super_admin})
    else:
        fm = CreateUserForm()
    return render(request, 'account/signup/signup.html', {'form': fm})
