from django.conf.urls import patterns, url
from django.contrib.auth.views import password_reset_complete, password_reset_confirm, password_reset, password_change
import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^add_category/$', views.add_category, name='add_category'),
                       url(r'^(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
                       url(r'^restricted/$', views.restricted, name='restricted'),
                       url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, name='password_reset_confirm'),
                       url(r'^reset/complete/$', password_reset_complete, name='password_reset_complete'),
                       url(r'^password/reset/$', password_reset, {'post_reset_redirect': '/rango/'}, name='reset_password'),
                       url(r'^password/change/$', password_change, {'post_change_redirect': '/rango/'}, name='change_password'),
                       url(r'^goto/', views.track_url, name='goto'),
                       url(r'^add_profile/$', views.register_profile, name='register_profile'),
                       url(r'^profile/$', views.profile, name='user_profile'),
                       )
