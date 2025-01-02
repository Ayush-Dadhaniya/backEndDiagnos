from django.urls import path
from . import views

urlpatterns = [
    path('predict_disease/', views.predict_disease, name='predict_disease'),
]