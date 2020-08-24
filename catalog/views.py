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

from catalog.forms import SignUp, Login
from webChat import settings

def home(request):
    return render(request, 'home.html')

def login(request):
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
                if user.is_active:
                    return redirect('chat_rooms')
                else:
                    return redirect('waitingConfirmation')
            else:
                messages.warning(request,'Por favor ingrese un nombre de usuario y contraseña correctos')
    return render(request, 'login.html', {'form_login': form_login})

@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def chat_rooms(request):
    return render(request, 'chat_rooms.html')

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
            #user.is_active = False
            #user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activación Cuenta'
            message = render_to_string('active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
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
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Gracias por su confirmación por correo electrónico. Ahora puede iniciar sesión en su cuenta')
    else:
        return HttpResponse('El enlace de activación no es válido.')