from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import JsonResponse

import logging
from ml_utils import id3tags
from ml_utils.emotion_extraction.music_reco_app2 import runMusicEmoReco
from ml_utils.feature_extraction.convert import convert_to_wav
from ml_utils.genre_classify.predict import predict_song
import ml_utils.feature_extraction.extractFeatures as ef
import shutil


def index(request):
    return render(request, 'analyser/index.html', {})


def upload_file(request):
    # TODO: Validate form on client side
    if request.method == 'POST' and request.FILES['music-input']:
        audio_file = request.FILES['music-input']
        fs = FileSystemStorage()
        filename = fs.save('analyser/uploaded_files/' + audio_file.name, audio_file)
        logging.error('FILENAME:' + filename)

        tags = id3tags.get_tags(filename)
        convert_to_wav(filename)

        return render(request, 'analyser/feature_home.html', {
            'uploaded_filename': filename,
            'show_loading_animation': True,
            'artist': tags['artist'],
            'title': tags['title'],
            'album': tags['album'],
        })
    return render(request, 'analyser/index.html')


def get_emotions(request):
    filename = request.GET.get('filename', None)
    if filename is None:
        logging.error(' Filename is null!')
    emotion_data = runMusicEmoReco(filename)
    emotion_data['emo_image_url'] = '../static/images/emoticons/' + emotion_data['emotion'] + '.svg'
    return JsonResponse(emotion_data)


def get_genre(request):
    filename = get_filename_from(request)
    wave_path = filename[:-3] + 'wav'
    data = {}
    data['genre'] = predict_song(wave_path)
    return JsonResponse(data)


def get_features(request):
    filename = get_filename_from(request)
    wave_path = filename[:-3] + 'wav'
    dest_base = '/static/images/'
    data = {}

    (wavedata, sample_rate, avg_wavedata) = ef.extract_main(wave_path)
    data['sample_rate'] = sample_rate

    (number_samples, length) = ef.general_features(wavedata, sample_rate)
    data['number_samples'] = number_samples

    ef.plot_waveform(wavedata)
    data['wav-image-url'] = dest_base + 'wavedata.png'

    ef.plot_fourier(wavedata, sample_rate)
    data['fourier-image-url'] = dest_base + 'fourier.png'

    data['zero-crossing'] = ef.zero_crossing_rate(avg_wavedata, number_samples)

    data['rms'] = ef.root_mean_square(avg_wavedata, sample_rate)
    data['rms-image-url'] = dest_base + 'rms.png'

    data['centroid'] = ef.spectral_centroid(avg_wavedata, sample_rate)
    data['centroid-image-url'] = dest_base + 'spectral_centroid.png'

    data['flux'] = ef.spectral_flux(avg_wavedata, sample_rate)
    data['flux-image-url'] = dest_base + 'spectral_flux.png'

    data['roll'] = ef.spectral_rolloff(avg_wavedata, sample_rate)
    data['roll-image-url'] = dest_base + 'spectral_roll.png'

    return JsonResponse(data)

def get_filename_from(request):
    filename = request.GET['filename']
    if filename is None:
        logging.error(' Filename is null!')
    return filename
