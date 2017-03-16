import warnings
warnings.filterwarnings('ignore')
# numerical processing and scientific libraries
import numpy as np
# signal processing
from scipy.io import wavfile

# general purpose

# plotting
# Classification and evaluation
# general purpose
# plotting
#utility file
import utility



# np.set_printoptions(threshold=np.nan)

'''
  sampling of wav file. sound pressure values are mapped to integer values that can range from -2^15 to (2^15)-1. 
  Returns one index for left speaker and other for right speaker
'''
def extract_main(path):
  samplerate, wavedata = wavfile.read(path)
  avg_wavedata = avg_wavdata = np.mean(wavedata , axis=1)
  return (wavedata, samplerate, avg_wavedata)

'''
returns general information about the audio file
num_samples: number of samples
length: length of audio sample taken
 '''
def general_features(wavedata, samplerate) :
  num_samples = wavedata.shape[0]
  length = num_samples/samplerate
  return(num_samples, length)

'''
it plots the values mapped by wave file and time
output file => wavedata.png
'''
def plot_waveform(wavedata) :
  utility.show_stereo_waveform(wavedata,"analyser/static/images/wavedata.png")

'''
it plots the fourier transform
output=> fourier.png
'''
def plot_fourier(wavedata, samplerate) :
  utility.plotstft(wavedata, samplerate, "analyser/static/images/fourier.png")

'''
Zero Crossing Rate It represents the number of times the waveform crosses
0. It usually has higher values for highly percussive sounds like those in metal
and rock.
'''
def zero_crossing_rate(wavedata, number_of_samples) :
  zero_crossings = 0
  for i in range(1, number_of_samples):
    if ( wavedata[i - 1] <  0 and wavedata[i] >  0 ) or ( wavedata[i - 1] >  0 and wavedata[i] <  0 ) or ( wavedata[i - 1] != 0 and wavedata[i] == 0):
      zero_crossings += 1

  zero_crossing_rate = zero_crossings / float(number_of_samples - 1)

  return zero_crossing_rate

'''
equivalent heating energy
output plot => rms.png
'''
def root_mean_square(wavedata, sample_rate, block_length = 2048):

  # how many blocks have to be processed?
  num_blocks = int(np.ceil(len(wavedata)/block_length))
  # when do these blocks begin (time in seconds)?
  timestamps = (np.arange(0,num_blocks - 1) * (block_length / float(sample_rate)))
  rms = []
  for i in range(0,num_blocks-1):
    start = i * block_length
    stop  = np.min([(start + block_length - 1), len(wavedata)])
    rms_seg = np.sqrt(np.mean(wavedata[start:stop]**2))
    rms.append(rms_seg)

  rms = np.asarray(rms)
  timestamp = np.asarray(timestamps)
  utility.show_feature_superimposed(wavedata,sample_rate, rms, timestamp,"analyser/static/images/rms.png",squared_wf=False);
  return  np.mean(rms)

'''
Spectral Centroid: It describes where the centre of mass for sound is. It
  essentially is the weighted mean of the frequencies present in the sound. Consider
  two songs, one from blues and one from metal. A blues song is generally
  consistent throughout it length while a metal song usually has more frequencies
  accumulated towards the end part. So spectral centroid for blues song will lie
  somewhere near the middle of its spectrum while that for a metal song would
  usually be towards its end.
'''
def spectral_centroid(wavedata,sample_rate, window_size = 2048):
  magnitude_spectrum = utility.stft(wavedata, window_size)
  timebins, freqbins = np.shape(magnitude_spectrum)
  # when do these blocks begin (time in seconds)?
  timestamps = (np.arange(0,timebins - 1) * (timebins / float(sample_rate)))
  sc = []
  for t in range(timebins-1):
    power_spectrum = np.abs(magnitude_spectrum[t])**2
    sc_t = np.sum(power_spectrum * np.arange(1,freqbins+1)) / np.sum(power_spectrum)
    sc.append(sc_t)
  sc = np.asarray(sc)
  sc = np.nan_to_num(sc)
  timestamps = np.asarray(timestamps)
  utility.show_feature_superimposed(wavedata,sample_rate, sc, timestamps,"analyser/static/images/spectral_centroid.png", squared_wf=False)
  return  np.mean(sc)


'''
Spectral flux:
squared differences in frequency distribution of two successive time frames
measures the rate of local change in the spectrum
'''
def spectral_flux(wavedata, sample_rate, window_size = 1024):
  # convert to frequency domain
  magnitude_spectrum = utility.stft(wavedata, window_size)
  timebins, freqbins = np.shape(magnitude_spectrum)
  # when do these blocks begin (time in seconds)?
  timestamps = (np.arange(0,timebins - 1) * (timebins / float(sample_rate)))
  sf = np.sqrt(np.sum(np.diff(np.abs(magnitude_spectrum))**2, axis=1)) / freqbins
  sf =  sf[1:]
  timestamps = np.asarray(timestamps)
  utility.show_feature_superimposed(wavedata,sample_rate, sf, timestamps,"analyser/static/images/spectral_flux.png", squared_wf=False)
  return np.mean(sf)

'''
 SPECTRAL ROLLOFF
  It is a measure of the shape of the signal. It represents
  the frequency at which high frequencies decline to 0. To obtain it, we have to
  calculate the fraction of bins in the power spectrum where 85% of its power is
  at lower frequencies.
'''
def spectral_rolloff(wavedata,  sample_rate,window_size=1024,k=0.85):
  # convert to frequency domain
  magnitude_spectrum = utility.stft(wavedata, window_size)
  power_spectrum     = np.abs(magnitude_spectrum)**2
  timebins, freqbins = np.shape(magnitude_spectrum)
  # when do these blocks begin (time in seconds)?
  timestamps = (np.arange(0,timebins - 1) * (timebins / float(sample_rate)))
  sr = []
  spectralSum    = np.sum(power_spectrum, axis=1)
  for t in range(timebins-1):
      # find frequency-bin indeces where the cummulative sum of all bins is higher
      # than k-percent of the sum of all bins. Lowest index = Rolloff
      sr_t = np.where(np.cumsum(power_spectrum[t,:]) >= k * spectralSum[t])[0][0]
      sr.append(sr_t)
  sr = np.asarray(sr).astype(float)
  # convert frequency-bin index to frequency in Hz
  sr = (sr / freqbins) * (sample_rate / 2.0)
  timestamps =  np.asarray(timestamps)
  utility.show_feature_superimposed(wavedata,sample_rate, sr, timestamps,"analyser/static/images/spectral_roll.png", squared_wf=False)
  return np.mean(sr)

