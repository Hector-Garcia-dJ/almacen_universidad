"""
URL Configuration for almacen_app.

This module defines the URL patterns for the almacen_app application.
"""
from django.contrib import admin
from django.urls import path
from . import views

APP_NAME = 'almacen_app'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('admin_panel/', admin.site.urls, name='admin_panel'),
    path('registrar_persona/', views.registrar_persona, name='registrar_persona'),
    path('registrar_productos/', views.registrar_productos_view, name='registrar_productos'),
    path('consultar-productos/', views.consultar_productos, name='consultar_productos'),
    path('solicitudes/', views.solicitudes_view, name='solicitudes'),
    path('generar_reportes/', views.generar_reportes_view, name='generar_reportes'),
]
