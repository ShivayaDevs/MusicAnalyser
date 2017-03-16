from django.conf.urls import url
import views

app_name = 'analyser'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload_file, name='upload'),
    url(r'^features/', views.features_home, name='feature_home'),
    url(r'^ajax/emotion', views.fetch_emotions, name='emotion_recognition'),
]