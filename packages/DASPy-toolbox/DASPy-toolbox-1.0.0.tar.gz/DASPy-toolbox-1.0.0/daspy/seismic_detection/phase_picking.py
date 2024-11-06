# Purpose: Pick phases for events
# Author: Minzhe Hu
# Date: 2024.8.30
# Email: hmz2018@mail.ustc.edu.cn
import numpy as np
from scipy.stats import kurtosis, skew
from obspy.signal.trigger import classic_sta_lta, trigger_onset
from daspy.basic_tools.preprocessing import normalization


def sta_lta_map(data, fs, sw=0.5, lw=5):
    cft = np.zeros_like(data)
    for ch, d in enumerate(data):
        cft[ch] = classic_sta_lta(d, nsta=round(sw * fs), nlta=round(lw * fs))

    return cft

def kurto_map(data, fs, win=3, diff=True, norm=True):
    nch, nt = data.shape
    w = round(win * fs)
    kts = np.zeros((nch, nt-w))
    for t in range(w, nt):
        kts[:, t - w] = kurtosis(data[:, t - w:t], axis=1)

    pre_nt = w
    if diff:
        kts = np.abs(np.diff(kts, axis=1))
        pre_nt += 1
    if norm:
        kts = normalization(kts)

    kts = np.hstack((np.zeros((nch, pre_nt)), kts))
    return kts

def skew_map(data, fs, win=3, diff=True, norm=True):
    nch, nt = data.shape
    w = round(win * fs)
    kts = np.zeros((nch, nt-w))
    for t in range(w, nt):
        kts[:, t - w] = skew(data[:, t - w:t], axis=1)

    pre_nt = w
    if diff:
        kts = np.abs(np.diff(kts, axis=1))
        pre_nt += 1
    if norm:
        kts = normalization(kts)

    kts = np.hstack((np.zeros((nch, pre_nt)), kts))
    return kts


def map_picking(hot_map, thres1=5, thres2=5, choose_max=True, min_dsp=None):
    pick = []
    for ch, arr in enumerate(hot_map):
        onsets = trigger_onset(arr, thres1=thres1, thres2=thres2)
        if len(onsets) != 0:
            for s, e in onsets:
                if min_dsp is not None:
                    if e - s < min_dsp:
                        continue
                if choose_max:
                    pick.append([ch, np.argmax(arr[s:e+1]) + s])
                else:
                    pick.append([ch, s])

    return np.array(pick)
