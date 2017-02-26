# -*- coding: utf-8 -*-

"""
This is the original file that the client sent me.

When I (Omar Trejo) solved this problem, I chose
not to reuse this code, and start from scratch.
"""

import wave
import numpy as np
import matplotlib.pyplot as plt
#import utility
import scipy
import scipy.signal
import numba
import scipy.io.wavfile as wavfile

import scikits.audiolab as audiolab





f = audiolab.Sndfile("/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01/SR001MS.wav", 'r')
#f = wave.open("/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01/SR001MS.wav",'r')
data = np.array(f.read_frames(f.nframes), dtype=np.float64)
f.close()
rate = f.samplerate;
print("rate: ", rate)
wavfile.write("/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01/SROO1MSout.wav", rate, data)


with wave.open('/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01/SR001MSout.wav') as w:
    channels = w.getnchannels()
    fs = w.getframerate()
    assert w.getsampwidth() == 2
    data = w.readframes(w.getnframes())
    
    print("Initial Sampling Frequency: ", fs)
    print("Channels: ", channels)
    print("Length: ", len(data))

mic_audio = data
#sig = np.frombuffer(data, dtype='<i2').reshape(-1, channels)
#normalized = utility.pcm2float(sig, np.float64)
#mic_audio = normalized

plt.figure()
plt.plot(mic_audio)
plt.title("Original Signals")

#print("Length Normalized: ", (len(mic_audio)))

@numba.jit
def L(mic_audio):
    secs = len(mic_audio)/44100.0  # Number of seconds in mic_audio
    return (secs)
(secs) = L(mic_audio) 

(secs) = L(mic_audio)
print ("Secs in mic_audio: ", secs)

p2 = np.floor(np.log2(len(mic_audio)))
nextpow2 = np.power(2, p2-1)
print("Next power of 2: ", nextpow2)

mic_audio2 = mic_audio[0:nextpow2]
secs2 = len(mic_audio2)/44100.0

@numba.jit
def M(secs2):
    samps = secs2*1024.0 # Number of samples to downsample
    #samps = secs*256.0 # Number of samples to downsample
    return (samps)
    
(samps) = M(secs2)
print ("# of samples to downsample: ", samps)

@numba.jit
def N(mic_audio2, samps):
    Y = scipy.signal.resample(mic_audio2, samps) 
    return (Y)

(Y) = N(mic_audio2, samps)

fs2 = samps/secs2
print("fs2: ", fs2)   # Sampling frequency of downsampled signal (Y)
print("Length Y: ", len(Y))  # Number of samples in Y


## ----- PLOT data ----- ##
plt.figure()
plt.plot(mic_audio)
plt.hold()
plt.plot(Y, color = 'm', linestyle=':')
plt.title("Original vs Downsampled Signals")

plt.figure()
plt.plot(mic_audio[0:2000])
plt.hold()
plt.plot(Y[0:2000])
plt.title("Original vs Downsampled Signals")

#--------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#@numba.jit
#def samp(mic_audio):
#    secs = len(mic_audio)/44100.0
#    samps = secs*1024.0
#    Y = scipy.signal.resample(mic_audio, samps)
#    return (samps, secs, Y)
#
#(samps, secs, Y) = samp(mic_audio)
#  

#secs = len(mic_audio)/44100.0 # Number of seconds in signal X
#samps = secs*1024   # Number of samples to downsample
#Y = scipy.signal.resample(mic_audio, samps)
#def secs(X):
#    return len(mic_audio)/44100
#    
#@numba.jit
#def samps(secs):
#    return secs*1024
#    
#@numba.jit
#def Y(samps):
#    return scipy.signal.resample(mic_audio, samps)





#
#
#plt.figure()
#mic_audioslice = mic_audio[0:2646000]
#plt.plot(mic_audioslice)
#
#plt.figure()
#mic_audioslice2 = mic_audio[0:1323000]
#plt.plot(mic_audioslice2)
#
#plt.figure()
#mic_audioslice3 = mic_audio[0:44100]
#plt.plot(mic_audioslice3)
#
#plt.figure()
#mic_audioslice4 = mic_audio[0:22050]
#plt.plot(mic_audioslice4)

#with wave.open('/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01/SR001XY.wav') as w2:
#    channels2 = w2.getnchannels()    
#    wave.Wave_write(w2)
#   
#    fs_mic = w2.setframerate(1024)
#    fs2 = w2.getframerate()
#    assert w2.getsampwidth() == 2
#    data2 = w2.readframes(w2.getnframes())
#    
#    print("New Sampling Frequency: ", fs2)
#    #print("Channels: ", channels2)
#    print(len(data2))
#    
#
#sig2 = np.frombuffer(data2, dtype='<i2').reshape(-1, channels2)
#
#normalized2 = utility.pcm2float(sig2, np.float32)
#normchunk2 = normalized2[0:10240]
#mic_audio2 = normchunk2
##plt.plot(normchunk)
#plt.plot(mic_audio2)









########################## Drafts #####################################
#import wave
#import audioop
#import scipy
#from scipy import
##
#from path import Path
#d = Path('/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01')
#for f in d.files('*.wav'):
#scipy.io.wavfile.read('/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01/SR001XY.wav') 

#import wave



#XY = wave.open('/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01/SR001XY.wav')
#wave.Wave_read.getnchannels(XY)
#wave.Wave_read.getframerate(XY)
#wave.Wave_read.getparams(XY)


#-----------------------------------
#import numpy as np
#import wave 
#import struct
#import sys
#
#def wav_to_floats(wave_file):
#    w = wave.open(wave_file)
#    astr = w.readframes(w.getnframes())
#    a = struct.unpack("%ih" % (w.getnframes()* w.getnchannels()), astr)
#    a = [float(val)/pow(2,15) for val in a]
#    return a
#    
#signal = wav_to_floats(sys.argv[1])
#print ("read "+str(len(signal))+" frames")
#print ("in the range "+str(min(signal))+" to "+str(min(signal)))
#--------------------------------------------

#import wavefile

# returns the contents of the wav file as a double precision float array
#def wav_to_floats(filename = 'SR001XY.wav'):
#    path = '/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01/'
#    w = wavefile.load(path+filename)
#
#
#    return w[1][0]
#
#signal = wav_to_floats(sys.argv[1])
#print ("read "+str(len(signal))+" frames")
#print  ("in the range "+str(min(signal))+" to "+str(min(signal)))


#----------------this works-------------
#import numpy as np
#from scipy.io import wavfile  ## This works!! but data is in integer format
#fs, data = np.array(wavfile.read('/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01/SR001XY.wav'))
#----------------------------------------

#import utility
#from scipy.io import wavfile
#from utility import pcm2float
#
#fs, data = wavfile.read('/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01/SR001XY.wav')
#normalized = pcm2float(data,'float32')
#
#print ("sampling rate = {} Hz, length = {} samples, channels = {}".format(fs, *data.shape))
#print (data)
#plot(data)
#----------------------------------------------


#/////////////// From https://github.com/mgeier/python-audio/blob/master/audio-files/audio-files-with-wave.ipynb /////////
#import matplotlib.pyplot as plt
#import numpy as np
#import wave
#
#
#with wave.open('/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01/SR001XY.wav') as w:
#    framerate = w.getframerate()
#    frames = w.getnframes()
#    channels = w.getnchannels()
#    width = w.getsampwidth()
#    print("sampling rate:", framerate, "Hz, length:", frames, "samples,",
#          "channels:", channels, "sample width:", width, "bytes")
#    
#    data = w.readframes(frames)
#
#print (len(data))
#print(type(data))
#print (data)
#
#sig = np.frombuffer(data, dtype='B')
#print ("signal B: ", sig)
#
#sig = np.frombuffer(data, dtype='<i2').reshape(-1, channels)
#print ("signal i2: ", sig)
#plt.plot(sig)
#
#print ("sig base is data: ", sig.base.base is data)
#print ("Flags", sig.flags)
#
#import utility
#normalized = utility.pcm2float(sig, 'float32')
#plt.plot(normalized)
#
#print ("normalized flags: ", normalized.flags)
#
#with wave.open('/Users/<username_obfuscated>/LocalDura/AUDIO/tests/audio_test_2/mic/4CH/FOLDER01/SR001XY.wav') as w:
#    framerate = w.getframerate()
#    frames = w.getnframes()
#    channels = w.getnchannels()
#    width = w.getsampwidth()
#    print("sampling rate = {framerate} Hz, length = {frames} samples, channels = {channels}, sample width = {width} bytes".format(**locals()))
#    
#    data = w.readframes(frames)
#
#
#    #assert width == 3
#    temp = bytearray()
#
#for i in range(0, len(data), 3):
#    temp.append(0)
#    temp.extend(data[i:i+3])
#
## Using += instead of .extend() may be faster
## (see https://youtu.be/z9Hmys8ojno?t=35m50s).
## But starting with an empty bytearray and
## extending it on each iteration might be slow, anyway.
## See further below for how to reserve all necessary memory in the beginning.
#
#    four_bytes = np.frombuffer(temp, dtype='B').reshape(-1, 4)
#    four_bytes
#
#
#    sig = np.frombuffer(temp, dtype='<i4').reshape(-1, channels)
#    sig
#
#
#normalized = utility.pcm2float(sig, 'float32')
#plt.plot(normalized)
#//////////////////////////////////////////////////////////////////////////




#    frames = audioop.reverse(frames, params.sampwidth)
#
#    with wave.open(d/'SR0001XY.wav', 'wb') as XY:
#        XY.setparams(params)
#        XY.writeparams(frames)
#        
        
    
    
