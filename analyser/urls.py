from django.conf.urls import url
import views

app_name = 'analyser'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload_file, name='upload'),
    url(r'^ajax/emotion', views.get_emotions, name='emotion'),
    url(r'^ajax/genre', views.get_genre, name='genre'),
    url(r'^ajax/features', views.get_features, name='features'),
]