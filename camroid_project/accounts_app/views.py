# Create your views here.

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from .utils import generate_token
from django.conf import settings


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

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
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['confirm_password']

        if password1 == password2:
            if User.objects.filter(username=username, is_active=True).exists():
                messages.warning(request, "Username already taken")
                print("Username already taken")
                return redirect('register')
            elif User.objects.filter(email=email, is_active=True).exists():
                messages.warning(request, "Email already exists")
                print("Email already exists")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)

                email_subject = '[CAMROID] Please verify your email address for account activation'
                message = render_to_string('activate.html',
                                           {'user': user,
                                            'domain': current_site.domain,
                                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                            'token': generate_token.make_token(user)
                                            }
                                           )

                email_message = EmailMessage(
                    email_subject,
                    message,
                    'snegi8005@gmail.com',
                    [email]
                )
                email_message.content_subtype = "html"
                email_message.send()

                messages.success(request, 'Activation link has been send to your email')
                print("user created")
                return redirect('login')
        else:
            print("Password not matched")
            messages.info(request, "Password not matched")
            return redirect('register')
        return redirect('/')
    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            print('uid',uid)
            user= User.objects.get(pk=uid)
        except Exception as identifier:
            user=None

        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.add_message(request,messages.INFO, 'account activated successfully')
            return redirect('login')
        return render(request, 'activate_fail.html', status=401)
