from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views
from .api import (
    VueloViewSet,
    PasajeroViewSet,
    ReservaViewSet,
    AvionViewSet,
    BoletoViewSet,
)

# ===============================
# 🔹 Router API DRF
# ===============================
router = DefaultRouter()
router.register(r'vuelos', VueloViewSet, basename='vuelo')
router.register(r'pasajeros', PasajeroViewSet, basename='pasajero')
router.register(r'reservas', ReservaViewSet, basename='reserva')
router.register(r'aviones', AvionViewSet, basename='avion')
router.register(r'boletos', BoletoViewSet, basename='boleto')

# ===============================
# 🔹 Configuración Swagger / ReDoc
# ===============================
schema_view = get_schema_view(
    openapi.Info(
        title="API Sistema de Aerolínea",
        default_version='v1',
        description="Documentación interactiva del sistema de gestión de aerolínea",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contacto@aerolinea.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# ===============================
# 🔹 URLs web tradicionales
# ===============================
web_urls = [
    path('', RedirectView.as_view(pattern_name='vuelos_list', permanent=False)),

    path('vuelos/', views.vuelos_list, name='vuelos_list'),
    path('vuelos/<int:vuelo_id>/reservar/', views.reservar_vuelo, name='reservar_vuelo'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('cancelar-reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),

    # Login y Logout con vistas genéricas
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Registro de usuario
    path('registro/', views.registro, name='registro'),

    # Generación de boleto PDF
    path('reserva/<int:reserva_id>/boleto/', views.generar_boleto_pdf, name='generar_boleto_pdf'),
]

# ===============================
# 🔹 URLs API REST
# ===============================
api_urls = [
    path('', include(router.urls)),
]

# ===============================
# 🔹 URLs finales + Swagger
# ===============================
urlpatterns = web_urls + [
    path('api/', include(api_urls)),

    # Documentación Swagger / Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
