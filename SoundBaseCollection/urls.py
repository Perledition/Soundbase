from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^electronic/$', views.ElectroView.as_view(), name='electronic'),
    url(r'^rock/$', views.RockView.as_view(), name='rock'),
    url(r'^jazz/$', views.JazzView.as_view(), name='jazz')
]
