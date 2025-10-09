from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from home.views import RegisterView, LogoutView
import sentry_sdk
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Función de prueba de Sentry
def prueba_sentry(request):
    sentry_sdk.capture_message("Sentry funcionando en Django")
    return HttpResponse("Mensaje enviado a Sentry")

# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Aerolínea",
        default_version='v1',
        description="Documentación API REST de la aerolínea",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Rutas de i18n
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  
]

# Rutas de API REST y documentación
urlpatterns += [
    path('api/', include('gestionVuelos.urls_api')),           # Endpoints API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # JWT token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# Rutas tradicionales con i18n_patterns
urlpatterns += i18n_patterns(
    path('', lambda request: redirect('gestionVuelos:home'), name='root_redirect'),
    path('admin/', admin.site.urls),
    path('gestionVuelos/', include(('gestionVuelos.urls', 'gestionVuelos'), namespace='gestionVuelos')),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', RegisterView.as_view(), name='registro'),
)

