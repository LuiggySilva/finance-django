from django.urls import path
from . import views

app_name = "planejamento"

urlpatterns = [
    path('definir_planejamento/', views.definir_planejamento, name="definir_planejamento"),
    path('atualizar_valor_categoria/<int:id>', views.atualizar_valor_categoria, name="atualizar_valor_categoria"),
    path('ver_planejamento/', views.ver_planejamento, name="ver_planejamento"),
]