from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('vuelos/', views.vuelos_list, name='vuelos_list'),
    path('vuelos/<int:vuelo_id>/reservar/', views.reservar_vuelo, name='reservar_vuelo'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('cancelar-reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),

    # Login y Logout con las vistas genéricas de Django
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Registro personalizado
    path('registro/', views.registro, name='registro'),
]
