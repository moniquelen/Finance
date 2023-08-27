from django.urls import path
from . import views

urlpatterns = [
    path('definir_planejamento/', views.definir_planejamento, name="definir_planejamento"),
]