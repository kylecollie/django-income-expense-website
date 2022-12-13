import json
from validate_email import validate_email
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View



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
                
                # send activation email

                # path to view
                # - get domain we are on
                domain = get_current_site(request).domain()
                
                # - encode uid
                uidb64 = force_bytes(urlsafe_base64_encode(user.pk))

                # - token
                

                # - relative url to verification
                link = reverse('activate', kwargs = {'uidb64':uidb64, 'token':token})

                email_subject = 'Activate your account'
                email_body = 'Test body'
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email],
                )
                
                email.send(fail_silently=True)
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')
        
        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('login')