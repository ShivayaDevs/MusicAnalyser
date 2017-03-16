import numpy as np
import os
import scipy.io.wavfile

from scikits.talkbox.features import mfcc
from sklearn.externals import joblib


def predict_song(wavfile):
    sampling_rate, song_array = scipy.io.wavfile.read(wavfile)
    song_array[song_array == 0] = 1
    ceps, mspec, spec = mfcc(song_array)
    base_wav, ext = os.path.splitext(wavfile)
    data_wav = base_wav + ".ceps"
    np.save(data_wav, ceps)

    # features
    X = []
    Y = []
    ceps = np.load(data_wav + ".npy")
    num_ceps = len(ceps)
    X.append(np.mean(ceps[int(num_ceps * 1 / 10): int(num_ceps * 9 / 10)], axis=0))

    # prediction
    # print predict_file(X)
    genre_list = ["country", "hiphop", "metal", "pop", "reggae", "rock"]

    clf = joblib.load('./analyser/ml_utils/genre_classify/model_ceps.pkl')
    index = clf.predict(X)
    return genre_list[index[0]]
