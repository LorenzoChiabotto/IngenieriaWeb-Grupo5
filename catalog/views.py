from django.contrib.auth.models import User, auth
from django.contrib import messages
from webChat import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .login_form import SignUpForm

UserModel = get_user_model()

from django.shortcuts import render,redirect



def home(request):
    name = 'Manu'
    apellid = 'Ellocodelrenderizado'

    return render(request, 'home.html', {'prueba_manuel': name,'loco':apellid})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        user = request.POST['ingreso']
        password1 = request.POST['pass1']
        user = auth.authenticate(username=user, password=password1)
        print(user)
        if user is not None:
            if user.is_active:
                #Ya confirmo la cuenta y cumple las condiciones esperadas
                return redirect('chat_rooms')
            else:
                # No tiene la cuenta activa
                return redirect('login')
        else:
            messages.warning(request,'Por favor ingrese un nombre de usuario y contraseña correctos')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
def chat_rooms(request):
    return render(request, 'chat_rooms.html')

def waitingConfirmation(request):
    return render(request, 'waitingConfirmation.html')
def active_email(request):
    return render(request, 'active_email.html')
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    if request.method == 'POST':
        username = request.POST["usuario"]
        mail = request.POST["mail"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        print(username)
        print(mail)
        print(pass1)
        if (pass1 == pass2):
            user = User.objects.create_user(username, mail, pass1)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activación Cuenta'
            message = render_to_string('active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [mail]
            send_mail(mail_subject, message, email_from, recipient_list)
            return render(request, 'waitingConfirmation.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
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