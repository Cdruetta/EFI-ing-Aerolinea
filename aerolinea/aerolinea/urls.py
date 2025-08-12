from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from home.views import RegisterView, LogoutView
import sentry_sdk
from django.http import HttpResponse

def prueba_sentry(request):
    sentry_sdk.capture_message("✅ Sentry funcionando en Django")
    return HttpResponse("Mensaje enviado a Sentry")

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  
]

urlpatterns += i18n_patterns(
    path('', lambda request: redirect('gestionVuelos:home'), name='root_redirect'),
    path('admin/', admin.site.urls),
    path('gestionVuelos/', include(('gestionVuelos.urls', 'gestionVuelos'), namespace='gestionVuelos')),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', RegisterView.as_view(), name='registro'),
)
