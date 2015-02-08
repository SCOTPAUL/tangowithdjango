from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import password_reset_complete
from registration.backends.simple.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
import settings


# Send the newly registered user to /rango/
class MyRegistrationView(RegistrationView):
    # Ensure email uniqueness to allow for password reset
    form_class = RegistrationFormUniqueEmail

    def get_success_url(self, request, user):
        return '/rango/'


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
         {'document_root': settings.MEDIA_ROOT})
    )
