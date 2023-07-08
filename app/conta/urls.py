from django.urls import path
from . import views

app_name = "conta"

urlpatterns = [
    path('definir_conta/', views.definir_conta, name="definir_conta"),
    path('ver_contas/', views.ver_contas, name="ver_contas"),
]