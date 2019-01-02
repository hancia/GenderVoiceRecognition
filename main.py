import sys
import warnings
import scipy.io.wavfile
import numpy as np
from scipy.signal import decimate


def recognize():
    freq, voice = scipy.io.wavfile.read(sys.argv[1])
    t = len(voice) / freq

    if len(np.shape(voice)) == 2:
        voice = [s[0] for s in voice]

    mask = np.kaiser(len(voice), 5)
    voice = voice * mask

    base_sig = abs(np.fft.rfft(voice))
    sig = abs(np.fft.rfft(voice))

    for i in range(2, 6):
        dec_sig = decimate(base_sig, i)
        sig = sig[:len(dec_sig)] * dec_sig

    result = (np.argmax(sig[60:]) + 60) / t

    if result > 170:
        print("K")
    else:
        print("M")


if __name__ == '__main__':
    warnings.simplefilter("ignore")
    try:
        recognize()
    except:
        print("K")
