from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prediction/', views.prediction, name='prediction'),
    path('prediction/compute/', views.compute, name='compute'),
    path('prediction/resultats/', views.resultats, name='resultats'),
    path('france/', views.france, name='france'),
    path('france/<str:code_dept>/', views.departement, name='departement'),
    path('france/<str:code_dept>/<str:nom_ville>/', views.ville, name='ville'),
]
