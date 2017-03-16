from django.core.files.storage import FileSystemStorage
from django.shortcuts import render


def index(request):
    return render(request, 'analyser/index.html', {})


def upload_file(request):
    if request.method == 'POST' and request.FILES['music-input']:
        audio_file = request.FILES['music-input']
        fs = FileSystemStorage()
        filename = fs.save(audio_file.name, audio_file)
        uploaded_file_url = fs.url(filename)

        return render(request, 'analyser/feature_home.html', {
            'uploaded_file_url': uploaded_file_url ,
            'show_loading_animation': True,
        })
    return render(request, 'analyser/index.html')


def features_home(request):
    return render(request, 'analyser/feature_home.html', { 'show_loading_animation': True})
