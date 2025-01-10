from django.http import HttpResponse
from cars.models import Car,Brand
from .forms import LoginForm,CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser, Wishlist, UserProfile
from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.views import View, generic
from django.contrib.auth import views as auth_views

import smtplib

@never_cache
def landing_page(request):
    cars = Car.objects.all()
    
    return render(request, 'landing_page.html', {
        'is_landing_page': True,
        'cars': cars,
    })


#USUARIOS

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()

        if form.cleaned_data.get('user_type') == 'worker':
            return redirect('assign_worker', kwargs={'worker_id': user.id})
        
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('login')

class ProfileView(generic.DetailView):
    model = CustomUser
    template_name = 'profile.html'

class ProfileUpdateView(generic.UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('landing_page')

class ProfileWorkerView(generic.DetailView):
    model = CustomUser
    template_name = 'profile_worker.html'

class ProfileWorkerUpdateView(generic.UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'profile_worker_update.html'
    success_url = reverse_lazy('lab')


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            logout(request)  # Cerrar sesión antes de iniciar sesión
            login(request, user)
            return HttpResponseRedirect(reverse('landing_page'))  # o 'landing_page' si tienes nombre de ruta para la landing
        else:
            messages.error(request, "Email o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # El usuario no estará activo hasta que confirme su email
            user.save()
            # # Enviar correo de confirmación
            uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
            token = default_token_generator.make_token(user)
            current_site = get_current_site(request)
            mail_subject = 'Confirma tu correo electrónico'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(user.email,mail_subject, message)

            return render(request,'registration/email_confirmation.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def send_mail(to, subject, body, from_mail=settings.DEFAULT_FROM_EMAIL, password=settings.EMAIL_HOST_PASS):
    from email.mime.text import MIMEText
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_mail
    msg['To'] = to
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_mail, password)
    s.sendmail(from_mail, [to], msg.as_string())
    s.quit()

def email_confirmation(request):
    return render(request, 'registration/email_confirmation.html')


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def get_users(self, email):
        return CustomUser.objects.filter(email=email)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        users = self.get_users(email)

        # Si no hay usuarios con el correo, no hacemos nada
        if not users:
            return self.render_to_response(self.get_context_data(form=form))

        # Procesar cada usuario encontrado
        for user in users:
            print(f"Procesando usuario: {user}")  # Imprimir el usuario completo para depuración

            # Verificar que `user.pk` no sea una lista ni otro tipo inesperado
            if isinstance(user.pk, list):
                print(f"Error: user.pk es una lista, valor: {user.pk}")
                return self.render_to_response(self.get_context_data(form=form))  # O manejar el error como sea necesario

            print(f"MAIL: {os.environ.get('MAIL')}")
            print(f"MAIL_PASSWORD: {os.environ.get('MAIL_PASSWORD')}")
            # Asegúrate de que `user.pk` es un valor correcto
            print(f"user pk: {user.pk}")  # Verificar el tipo y valor de `user.pk`
            # Usar `force_bytes` para convertir el ID a bytes
            uid = str(urlsafe_base64_encode(force_bytes(user.pk)))  # Asegúrate de que es una cadena
            print(f"UID generado: {uid}")  # Imprimir para verificar

            # Generar el token
            token = str(default_token_generator.make_token(user))  # Asegúrate de que es una cadena
            print(f"Token generado: {token}")  # Imprimir para verificar

            print(f"uid: {uid} (Tipo: {type(uid)})")
            print(f"token: {token} (Tipo: {type(token)})")
            print(f"email: {email} (Tipo: {type(email)})")
            # Preparar el asunto y el mensaje del correo
            subject = render_to_string(self.subject_template_name, {'user': user})
            subject = ''.join(subject.splitlines())

            message = render_to_string(self.email_template_name, {
                'user': user,
                'domain': get_current_site(self.request).domain,
                'site_name': get_current_site(self.request).name,
                'uid': str(uid),  # Asegúrate de que es una cadena
                'token': str(token), 
                'protocol': 'https' if self.request.is_secure() else 'http',
            })

            # Imprimir el email y su tipo para asegurarnos de que es una cadena
            print(f"Email: {email}")
            print(f"Valor de `email`: {email}")
            print(f"Tipo de `email`: {type(email)}")

            # Enviar el correo
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],  # Asegúrate de que esto sea una lista de un solo correo
            )
        return super().form_valid(form)

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'  

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'  
    success_url = reverse_lazy('password_reset_complete')  

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'  # Personaliza la plantilla si lo deseas

def user_registration_view(request):
    if request.method == "POST":

        subject = "Bienvenido a nuestro sitio"
        body = "Gracias por registrarte. Estamos emocionados de tenerte con nosotros."
        to_email = "user@example.com"  
        
        send_mail(subject, body, to_email)

        return HttpResponse("Registro completado y correo enviado.")
    
    return render(request, 'signup.html')


def email_confirmation(request):
    return render(request, 'registration/email_confirmation.html')

def activation_failed(request):
    return render(request, 'registration/activation_failed.html')

def activate(request, uidb64, token):
    try:
        # Decodificar UID y asegurarse de que es válido
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = get_user_model().objects.get(pk=int(uid))  # Asegúrate de que sea un entero
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
        print("Error al decodificar el UID o encontrar el usuario.")
    
    if user is not None:
        comprobacion = default_token_generator.check_token(user, token)
        
        if comprobacion:
            user.is_active = True
            user.save()
            login(request, user, backend='users.backends.EmailBackend')
            return render(request, 'landing_page.html')
    
    return render(request, 'registration/activation_failed.html')

def logout_view(request):
    logout(request)
    return redirect('landing_page') 