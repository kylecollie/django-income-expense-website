import json
from validate_email import validate_email
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from .utils import token_generator



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
                domain = get_current_site(request).domain
                
                # - encode uid
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                # - token
                token = token_generator.make_token(user)

                # - relative url to verification
                link = reverse('activate', kwargs = {'uidb64':uidb64, 'token':token})

                activate_url = 'http://' + domain + link

                email_subject = 'Activate your account'
                email_body = 'Hi ' + user.username +'. Please use this link to verify your account.\n' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email],
                )
                
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')
        
        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            # import pdb; pdb.set_trace()
            user = User.objects.get(pk = id)
            
            if user.is_active:
                return redirect('login')
            
            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')
            
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except User.DoesNotExist:
            return redirect('register'+'?message='+'User not found')

        except Exception as ex:
            # import pdb; pdb.set_trace()
            return redirect('login')

        

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')