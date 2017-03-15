from django.conf.urls import url
import views

app_name = 'analyser'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload_file, name='upload')
]