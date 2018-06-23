from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('presentation/', views.presentation, name='presentation'),
    path('predictor/', views.predictor, name='predictor'),
    path('predictor/compute/', views.compute, name='compute'),
    path('predictor/results/', views.results, name='results'),
    path('france/', views.france, name='france'),
    path('france/<str:code_dept>/', views.departement, name='departement'),
    path('france/<str:code_dept>/<str:nom_ville>/', views.ville, name='ville'),
]
