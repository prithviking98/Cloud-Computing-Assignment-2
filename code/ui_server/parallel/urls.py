from django.urls import path

from parallel import views

app_name = 'parallel'

urlpatterns = [
	path('write/', views.write_handler, name='write_handler'),
	path('read/', views.read_handler, name='read_handler'),
	path('', views.home_html, name='home'),
	path('read_html/', views.read_html, name='read_html'),
	path('write_html/', views.write_html, name='write_html'),

]