# Create your views here.

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.http import JsonResponse
from validate_email import validate_email

from .utils import generate_token
import threading


def check_email_exists(request):

    email = request.GET.get("email")    
    email_exists = User.objects.filter(email=email, is_active=True).exists()

    return JsonResponse(email_exists, safe=False)


def check_username_notexists(request):

    username = request.GET.get("username")
    username_exists = not User.objects.filter(username=username, is_active=True).exists()

    return JsonResponse(username_exists, safe=False)


def check_email_notexists(request):

    email_exists = False
    email = request.GET.get("email")
    print(validate_email(email, verify=True))
    if validate_email(email, verify=True):
        email_exists = not User.objects.filter(email=email, is_active=True).exists()

    return JsonResponse(email_exists, safe=False)

# --------------------------------------------------------------------------------------------------

def login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username)
        print(password)
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            userdetail = User.objects.get(username=request.user.username)
            print('userdetail: ',userdetail)
            messages.info(request, 'Welcome, '+userdetail.username)
            # return render(request, 'myspace.html', {'user': userdetail})
            return redirect('myspace')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')

        context = {
            'values': request.POST
        }

        if password1 == password2:
            if User.objects.filter(username=username, is_active=True).exists():
                messages.warning(request, "Username already taken")
                print("Username already taken")
                return render(request, 'register.html', context)
            elif User.objects.filter(email=email, is_active=True).exists():
                messages.warning(request, "Email already exists")
                print("Email already exists")
                return render(request, 'register.html', context)
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain

                link = reverse('activate', kwargs={
                    'uidb64': uidb64, 'token': generate_token.make_token(user)
                })

                activate_url = "http://"+domain+link

                email_body = "Hi <b>" + user.username + "</b>,<br>To complete your sign up, we just need to verify your email address. Click below link to activate your account <br>" + activate_url + "."
                email_subject = '[CAMROID] Please verify your email address for account activation'


                email_message = EmailMessage(
                    email_subject,
                    email_body,
                    'noreplyuser97@gmail.com',
                    [email]
                )
                email_message.content_subtype = "html"
                EmailThreading(email_message).start()
                messages.success(request, 'Activation link has been send to your email')
                print("user created")
                return redirect('login')
        else:
            print("Password not matched")
            messages.info(request, "Password not matched")
            return render(request, 'register.html', context)
        return redirect('/')
    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=uid)

            if not generate_token.check_token(user, token):
                messages.add_message(request, messages.INFO, "Account already activated")
                return redirect('login')

            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, "Account activated successfully")
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'reset-password.html')

    def post(self, request):

        email = request.POST['email']

        context = {
            'values': request.POST
        }

        current_site = get_current_site(request)
        user = User.objects.filter(email=email)

        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            }

            link = reverse('reset-user-password', kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']
            })
            email_subject = '[CAMROID] Password reset link for your account'

            reset_url = "http://"+current_site.domain+link


            email_message = EmailMessage(
                email_subject,
                'Hi there, Please click the link below to reset your password \n' + reset_url,
                'noreplyuser97@gmail.com',
                [email]
            )

            EmailThreading(email_message).start()
            messages.success(request, "Reset password email has been sent.")
        else:
            messages.info(request, "Email does not exist")
            return render(request, 'reset-password.html', context)

        return render(request, 'reset-password.html')

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):

        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):

                messages.info(request, "Password link is expired, please request a new one")
                return render(request, 'reset-password.html')

        except Exception as identifier:
            pass

        return render(request, "set-new-password.html", context)

    def post(self, request, uidb64, token):

        context = {
            'uidb64': uidb64,
            'token': token
        }

        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if password != confirmpassword:
            messages.error(request, "Password do not match")
            return render(request, 'set-new-password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(request, "Password reset successfully")
            return redirect('login')
        except Exception as identifier:
            messages.warning(request, "Something went wrong")
            return render(request, "set-new-password.html", context)

        # return render(request, "set-new-password.html", context)

class EmailThreading(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send(fail_silently=False)
