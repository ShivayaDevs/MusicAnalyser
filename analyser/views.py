from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import JsonResponse

import logging
import os
from ml_utils.emotion_extraction.music_reco_app2 import runMusicEmoReco


def index(request):
    return render(request, 'analyser/index.html', {})


def upload_file(request):
    # TODO: Validate form on client side
    if request.method == 'POST' and request.FILES['music-input']:
        audio_file = request.FILES['music-input']
        fs = FileSystemStorage()
        filename = fs.save('analyser/uploaded_files/' + audio_file.name, audio_file)
        logging.error('FILENAME:' + filename)
        uploaded_file_url = fs.url(filename)

        return render(request, 'analyser/feature_home.html', {
            'uploaded_filename': filename,
            'show_loading_animation': False,
        })
    return render(request, 'analyser/index.html')


def features_home(request):
    return render(request, 'analyser/feature_home.html', {'show_loading_animation': True})


def get_emotion(filename):
    logging.error('starting parsing : ' + os.getcwd())
    # return True
    return runMusicEmoReco(filename)


def fetch_emotions(request):
    filename = request.GET.get('filename', None)
    if filename == None:
        logging.error(' Filename is null!')
    emotion_data = runMusicEmoReco(filename)
    emotion_data['emo_image_url'] = '../static/images/emoticons/' + emotion_data['emotion'] + '.svg'
    return JsonResponse(emotion_data)
