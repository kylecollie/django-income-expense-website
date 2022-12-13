from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from validate_email import validate_email 


# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email=data['email']
        
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email is in use, please use another one'}, status=409)

        return JsonResponse({'email_valid': True})
    
class UsernameValidation(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username is in use, choose another username'}, status=409)
        
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        # get user data
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        context = {
            'fieldValues': request.POST
        }
        
        # validate
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(request, 'Password is too short')
                    return render(request, 'authentication/register.html', context)

                # create user account
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                email_subject = 'Activate your account'
                email_body = ''
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    
                )
                
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')
        
        return render(request, 'authentication/register.html')