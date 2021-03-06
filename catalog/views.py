from django.contrib.auth.models import User, auth
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.core.mail import send_mail

from django.template.loader import render_to_string

from django.shortcuts import render,redirect

from django.http import HttpResponse

from datetime import timedelta
from django.utils import timezone

from catalog.forms import SignUp, Login 
from webChat import settings
from catalog.models import User_validable

def home(request):
    try:
        request.user = User_validable.objects.get(user=User.objects.get(username=request.user))
    except:
        return render(request, 'home.html')
    return redirect('chatRoom:roomsList')

def login(request):
    try:
        request.user = User_validable.objects.get(user=User.objects.get(username=request.user))
    except:
        pass
    auth.logout(request)
    form_login = Login()
    if request.method == 'POST':
        form_login = Login(request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data['user']
            password = form_login.cleaned_data['password']            
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                if User_validable.objects.get(user=(user)).is_confirmed:
                    return redirect('chatRoom:roomsList')
                else:
                    return redirect('catalog:waitingConfirmation')
            else:
                messages.warning(request,'Por favor ingrese un nombre de usuario y contraseña correctos')
    return render(request, 'login.html', {'form_login': form_login})

@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect('/')

def waitingConfirmation(request):
    return render(request, 'waitingConfirmation.html')


def signup(request):
    auth.logout(request)
    form_signup = SignUp()
    if request.method == 'POST':
        form_signup = SignUp(request.POST)
        if form_signup.is_valid():
            user = form_signup.cleaned_data['user']
            email = form_signup.cleaned_data['email']
            password = form_signup.cleaned_data['password']

            user = User.objects.create_user(user, email, password)

            token = default_token_generator.make_token(user)
            user_validable = User_validable.objects.create(user=user, is_confirmed=False)
            user_validable.token = token
            user_validable.save()

            current_site = get_current_site(request)
            mail_subject = 'Activación Cuenta'
            message = render_to_string('active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(mail_subject, message, email_from, recipient_list)

            return render(request, 'waitingConfirmation.html')

    return render(request, 'signup.html', {'form_signup': form_signup})

def activate(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        user_validable = User_validable.objects.get(user=(user))
        if(token == user_validable.token):
            user_validable.is_confirmed = True
            user_validable.save()
            return HttpResponse('Gracias por su confirmación por correo electrónico. Ahora puede iniciar sesión en su cuenta')
    
    return HttpResponse('El enlace de activación no es válido.')


@login_required(login_url='/login/')
def construction(request):
    try:
        request.user = User_validable.objects.get(user=User.objects.get(username=request.user))
    except:
        pass
    return render(request, 'construction.html')


@login_required(login_url='/login/')
def myProfile(request):
    try:
        request.user = User_validable.objects.get(user=User.objects.get(username=request.user))
    except:
        pass
    return render(request, 'myProfile.html')

def profile(request, user_pk):
    try:
        user_viewed = User_validable.objects.get(pk=user_pk)
    except:
        pass
    return render(request, 'profile.html',{"user":user_viewed})

