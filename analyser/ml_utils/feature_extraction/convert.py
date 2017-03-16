import os
import sys
import scipy.io.wavfile
import numpy as np
from scikits.talkbox.features import mfcc
#from classify import predict_file
from pydub import AudioSegment
from sklearn.externals import joblib

def convert_to_wav(path):
  song = AudioSegment.from_file(path)
  song = song[:30000]
  song.export(path[:-3]+"wav",format='wav')
  return path[:-3]+"wav"
  