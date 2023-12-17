from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages


def venta_pasajes(request, viaje_id):
    viaje = get_object_or_404(Viaje, pk=viaje_id)

    if request.method == 'POST':
        cantidad_pasajeros = int(request.POST.get('cantidad_pasajeros', 1))

        if cantidad_pasajeros <= viaje.cantidad_de_pasajeros_disponibles:
            ticket = Ticket(viaje=viaje, cantidad_de_pasajeros=cantidad_pasajeros)
            ticket.save()

            viaje.cantidad_de_pasajeros_disponibles -= cantidad_pasajeros
            viaje.save()

            # Redirige a la vista de confirmación de venta con el ID del ticket
            return redirect('confirmacion_venta', ticket_id=ticket.id)
        else:
            mensaje_error = 'No hay suficientes pasajes disponibles para la cantidad seleccionada.'
            return render(request, 'venta_pasajes.html', {'viaje': viaje, 'mensaje_error': mensaje_error})

    return render(request, 'venta_pasajes.html', {'viaje': viaje})
def confirmacion_venta(request, ticket_id):
    
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'confirmacion_venta.html', {'ticket': ticket})
class CalendarioOfertasView(View):
    template_name = 'calendario_ofertas.html'

    def get_context_data(self, **kwargs):
        context = {}
        # Obtén todas las ofertas
        viajes = Viaje.objects.all()
        context['viajes'] = viajes
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('calendario_ofertas')  # Redirige a la página después del inicio de sesión
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        full_name = request.POST.get('full_name')
        recovery_question = request.POST.get('recovery_question')

        # Verificar si las contraseñas coinciden
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html')

        # Crear un nuevo usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.save()

        # Autenticar al usuario y redirigir a la página después del registro
        user = authenticate(request, username=username, password=password)
        login(request, user)
        messages.success(request, 'Registro exitoso.')
        return redirect('login')  # Redirige a la página después del registro

    return render(request, 'registro.html')