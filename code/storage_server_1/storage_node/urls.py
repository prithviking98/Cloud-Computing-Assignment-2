from django.urls import path

from . import views

urlpatterns = [
    path('store/', views.store, name='store'),
    path('handoff/', views.handoff, name='handoff'),
]
