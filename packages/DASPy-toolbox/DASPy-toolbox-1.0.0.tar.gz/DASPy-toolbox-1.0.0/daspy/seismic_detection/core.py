import numpy as np
import daspy.basic_tools.visualization as DBV
from daspy.core import Section, DASDateTime
from daspy.seismic_detection.phase_picking import *

def plot(data, obj='waveform', title=None, cmap=None, vmax=None, vmin=None,
         **kwargs):
    if obj == 'pickmap':
        cmap = 'hot' if cmap is None else cmap
        vmax = np.percentile(abs(data), 99) if vmax is None else vmax
        vmin = np.percentile(abs(data), 80) if vmin is None else vmin
        title = obj
        obj = 'waveform'

    return DBV.plot(data, title=title, cmap=cmap, vmin=vmin, vmax=vmax,
                    **kwargs)

class DetectSection(Section):

    def __str__(self):
        describe = ''
        n = max(map(len, self.__dict__.keys()))
        for key, value in self.__dict__.items():
            if key in ['data', 'geometry', 'pickmap']:
                describe = '{}: shape{}\n'.format(key.rjust(n), value.shape) \
                    + describe
            elif key in ['dx', 'start_distance', 'gauge_length']:
                describe += '{}: {} m\n'.format(key.rjust(n), value)
            elif key == 'fs':
                describe += '{}: {} Hz\n'.format(key.rjust(n), value)
            elif key == 'start_time':
                if isinstance(value, DASDateTime):
                    describe += '{}: {}\n'.format(key.rjust(n), value)
                else:
                    describe += '{}: {} s\n'.format(key.rjust(n), value)
            elif key == 'pick':
                describe += '{}: {}\n'.format(key.rjust(n), len(value))
            else:
                describe += '{}: {}\n'.format(key.rjust(n), value)
        return describe
    
    __repr__ = __str__

    def plot(self, obj='waveform', kwargs_pro={}, **kwargs):
        if obj == 'pickmap':
            if 'data' not in kwargs.keys():
                if not hasattr(self, 'pick_map') or len(kwargs_pro):
                    self.calc_pickmap(**kwargs_pro)
                kwargs['data']= self.pickmap
            if 'cmap' not in kwargs.keys():
                kwargs['cmap'] = 'hot'
            if 'vmax' not in kwargs.keys():
                kwargs['vmax'] = np.percentile(abs(kwargs['data']), 99.9)
            if 'vmin' not in kwargs.keys():
                kwargs['vmin'] = np.percentile(abs(kwargs['data']), 95)
            if 'title' not in kwargs.keys():
                kwargs['title'] = obj
            obj = 'waveform'
        elif obj == 'phasepick':
            if 'data' not in kwargs.keys():
                kwargs['data']= self.data
            if 'pick' not in kwargs.keys():
                if not hasattr(self, 'pick') or len(kwargs_pro):
                    self.map_picking(**kwargs_pro)
                kwargs['pick'] = self.pick
                if len(kwargs['pick']):
                    kwargs['pick'][:, 0] -= self.start_channel

        super().plot(obj=obj, kwargs_pro=kwargs_pro, **kwargs)

    def calc_pickmap(self, method='sta_lta', **kwargs):
        if isinstance(method, str):
            method = [method]
        self.pickmap = np.zeros_like(self.data)
        for m in method:
            if m == 'sta_lta':
                self.pickmap += sta_lta_map(self.data, self.fs, **kwargs)
            elif m == 'kurto':
                self.pickmap += kurto_map(self.data, self.fs, **kwargs)
            elif m == 'skew':
                self.pickmap += skew_map(self.data, self.fs, **kwargs)
                
        return self.pickmap

    def map_picking(self, thres1=5, thres2=5, choose_max=False, min_dt=None,
                    **kwargs):
        if not hasattr(self, 'pick_map') or len(kwargs):
            self.calc_pickmap(**kwargs)

        pick = map_picking(self.pickmap, thres1=thres1, thres2=thres2,
                           choose_max=choose_max,
                           min_dsp=min_dt*self.fs).astype(float)
        if len(pick):
            pick[:, 0] += self.start_channel
            pick[:, 1] = pick[:, 1] / self.fs

        self.pick = pick
        return pick

    def symmetry_detection(self, win=5000):
            sec = self.copy()
            sec.normalization()
            win_ch = round(win / self.dx)
            cc = np.zeros(self.nch)
            for sch in range(self.nch):
                win_ch_use = min(win_ch, sch, sec.nch-sch-1)
                if win_ch_use > 0:
                    panel1 = sec.data[sch-win_ch_use:sch]
                    panel1 = panel1[::-1]
                    panel2 = sec.data[sch+1:sch+win_ch_use+1]
                    cc[sch] = np.sum(panel1 * panel2) / win_ch
            self.signal_channel = self.start_channel + np.argmax(cc)
            return cc / sec.nt

    @classmethod
    def from_section(clc, raw_sec):
        raw_dict = raw_sec.__dict__
        data = raw_dict.pop('data')
        return clc(data, **raw_dict)