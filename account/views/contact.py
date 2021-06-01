from django.http.response import HttpResponse
from account.decorators import unauthenticated_user
from django.shortcuts import render
from account.models import MyUser
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
@unauthenticated_user
def Contact(request):
    if request.method == 'GET':
        return render(request, 'account/contact/contact.html')
    else:
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')
        user = MyUser.objects.get(email=email)
        print(user)   
        temp = render_to_string('account/contact/contactus_msg.html',{'user':user,'message':message})
        try:
            email_to_send = EmailMessage(
            subject,
            temp,
            settings.EMAIL_HOST_USER,
            [email]
            )
            email_to_send.fail_silently = False
            email_to_send.send()
            print(user.first_name) 
            return HttpResponse(" Thank you. Your was sent successfully !! ")
            
        except Exception as e:
            return HttpResponse('Error!!  Failed to send Email. Please check your internet connection and try again')

        
