from django.urls import path

from . import views

urlpatterns = [
    path('store/', views.store, name='store'),
    path('handoff/', views.handoff, name='handoff'),
    path('handoff_return/', views.handoff_return, name='handoff_return'),
    path('handoff_return_trigger/', views.handoff_return_trigger, name='handoff_return_trigger'),
]
