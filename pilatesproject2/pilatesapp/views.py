from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
from django.http import HttpResponse

def email(request):    
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['j.locamuz@alumno.um.edu.ar',]   
    send_mail( subject, message, email_from, recipient_list, fail_silently=False)  
    return HttpResponse('email enviado desde jlocamuz@gmail.com')