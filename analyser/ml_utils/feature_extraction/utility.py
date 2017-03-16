'''
utility file contains all the basic plot and fourier transformation functions required by extraction file.
'''
import warnings
warnings.filterwarnings('ignore')

# numerical processing and scientific libraries
import numpy as np

# plotting
import matplotlib.pyplot as plt
from numpy.lib import stride_tricks

import numpy as np

PLOT_WIDTH  = 15
PLOT_HEIGHT = 3.5


def show_stereo_waveform(samples, output):

  fig = plt.figure(num=None, figsize=(PLOT_WIDTH, 5), dpi=72, facecolor='w', edgecolor='k')

  channel_1 = fig.add_subplot(211)
  channel_1.set_ylabel('Channel 1')
  #channel_1.set_xlim(0,song_length) # todo
  channel_1.set_ylim(-32768,32768)
  channel_1.plot(samples[:,0])

  channel_2 = fig.add_subplot(212)
  channel_2.set_ylabel('Channel 2')
  channel_2.set_xlabel('Time (s)')
  channel_2.set_ylim(-32768,32768)
  #channel_2.set_xlim(0,song_length) # todo
  channel_2.plot(samples[:,1])

  #plt.show();
  fig.savefig(output)
  plt.clf();


""" short time fourier transform of audio signal """
def stft(sig, frameSize, overlapFac=0.5, window=np.hanning):
  win = window(frameSize)
  hopSize = int(frameSize - np.floor(overlapFac * frameSize))
  
  # zeros at beginning (thus center of 1st window should be for sample nr. 0)
  samples = np.append(np.zeros(frameSize/2), sig)    
  # cols for windowing
  cols = np.ceil( (len(samples) - frameSize) / float(hopSize)) + 1
  # zeros at end (thus samples can be fully covered by frames)
  samples = np.append(samples, np.zeros(frameSize))
  cols = int(cols)
  frames = stride_tricks.as_strided(samples, shape=(cols, frameSize), strides=(samples.strides[0]*hopSize, samples.strides[0])).copy()
  frames *= win
  
  return np.fft.rfft(frames)    
    
""" scale frequency axis logarithmically """    
def logscale_spec(spec, sr=44100, factor=20.):
  timebins, freqbins = np.shape(spec)

  scale = np.linspace(0, 1, freqbins) ** factor
  scale *= (freqbins-1)/max(scale)
  scale = np.unique(np.round(scale))
  
  # create spectrogram with new freq bins
  newspec = np.complex128(np.zeros([timebins, len(scale)]))
  for i in range(0, len(scale)):
      if i == len(scale)-1:
          newspec[:,i] = np.sum(spec[:,int(scale[i]):], axis=1)
      else:        
          newspec[:,i] = np.sum(spec[:,int(scale[i]):int(scale[i+1])], axis=1)
  
  # list center freq of bins
  allfreqs = np.abs(np.fft.fftfreq(freqbins*2, 1./sr)[:freqbins+1])
  freqs = []
  for i in range(0, len(scale)):
      if i == len(scale)-1:
          freqs += [np.mean(allfreqs[int(scale[i]):])]
      else:
          freqs += [np.mean(allfreqs[int(scale[i]):int(scale[i+1])])]
  
  return newspec, freqs

""" plot spectrogram"""
def plotstft(samples, samplerate,output, binsize=2**10, plotpath=None, colormap="jet", ax=None, fig=None):
  s = stft(samples, binsize)
  sshow, freq = logscale_spec(s, factor=1.0, sr=samplerate)
  ims = 20.*np.log10(np.abs(sshow)/10e-6) # amplitude to decibel
  timebins, freqbins = np.shape(ims)
  if ax is None:
      fig, ax = plt.subplots(1, 1, sharey=True, figsize=(PLOT_WIDTH, 3.5))
  
  #ax.figure(figsize=(15, 7.5))
  cax = ax.imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")
  #cbar = fig.colorbar(cax, ticks=[-1, 0, 1], cax=ax)
  #ax.set_colorbar()
  ax.set_xlabel("time (s)")
  ax.set_ylabel("frequency (hz)")
  ax.set_xlim([0, timebins-1])
  ax.set_ylim([0, freqbins])
  xlocs = np.float32(np.linspace(0, timebins-1, 5))
  ax.set_xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
  ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 10)))
  ax.set_yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])
  
  if plotpath:
      plt.savefig(plotpath, bbox_inches="tight")
  else:
      fig.savefig(output)
      
  #plt.clf();
  b = ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate]
  return xlocs, b, timebins

def show_feature_superimposed(wavedata, samplerate, feature_data, timestamps, output, squared_wf=False):
  # plot waveform
  scaled_wf_y = ((np.arange(0,wavedata.shape[0]).astype(np.float)) / samplerate) * 1000.0
  if squared_wf:
      scaled_wf_x = (wavedata**2 / np.max(wavedata**2))
  else:
      scaled_wf_x = (wavedata / np.max(wavedata) / 2.0 ) + 0.5
  #scaled_wf_x = scaled_wf_x**2
  fig = plt.figure(num=None, figsize=(PLOT_WIDTH, 5), dpi=72, facecolor='w', edgecolor='k')
  plt.plot(scaled_wf_y, scaled_wf_x, color='lightgrey');
  # plot feature-data
  scaled_fd_y = timestamps * 1000.0
  scaled_fd_x = (feature_data / np.max(feature_data))
  plt.plot(scaled_fd_y, scaled_fd_x, color='r');
  fig.savefig(output)
  plt.clf();
    
