# Purpose: Locate earthquake location with body wave travel time
# Author: Minzhe Hu
# Date: 2024.6.5
# Email: hmz2018@mail.ustc.edu.cn
import os
import multiprocessing
import numpy as np
from pathlib import Path
from numpy.lib.stride_tricks import as_strided
from tqdm import tqdm
from obspy.taup.tau_model import TauModel
from obspy.taup import TauPyModel
from obspy.taup.taup_create import build_taup_model
from obspy.geodetics import locations2degrees



def calc_travel_time(model, elo, ela, edep, slo, sla, sdep):
    deg = locations2degrees(ela, elo, sla, slo)
    arrival = model.get_travel_times(source_depth_in_km=edep,
                                     receiver_depth_in_km=sdep,
                                     distance_in_degree=deg,
                                     phase_list=['p','P','s','S'])
    
    return arrival[0].time, arrival[1].time

def sliding_window_sum(matrix, half_win):
    shape = matrix.shape
    app = np.zeros((len(matrix), half_win))
    matrix = np.hstack((app, matrix, app))
    strides = (matrix.strides[1], matrix.strides[0], matrix.strides[1])
    windowed = as_strided(matrix[0:-2*half_win],
                          shape= (shape[1], shape[0], 2*half_win+1),
                          strides=strides)
    return np.sum(windowed, axis=(1,2))

def calc_max(pick_map, delay, mode='PS'):
    nch, nt = pick_map.shape
    if mode == 'P':
        delay = delay[:, 0]
        min_sp = delay.min()
        max_sp = delay.max()
        hotmap = np.zeros((nch, nt+max_sp-min_sp))
        for ch in range(nch):
            hotmap[ch, max_sp-delay[ch]:max_sp-delay[ch]+nt] = pick_map[ch]
    elif mode == 'S':
        delay = delay[:, 1]
        min_sp = delay.min()
        max_sp = delay.max()
        hotmap = np.zeros((nch, nt+max_sp-min_sp))
        for ch in range(nch):
            hotmap[ch, max_sp-delay[ch]:max_sp-delay[ch]+nt] = pick_map[ch]
    else:
        min_sp = delay.min()
        max_sp = delay.max()
        hotmap = np.zeros((nch, nt+max_sp-min_sp))
        for ch in range(nch):
            hotmap[ch, max_sp-delay[ch,0]:max_sp-delay[ch,0]+nt] += pick_map[ch]
            hotmap[ch, max_sp-delay[ch,1]:max_sp-delay[ch,1]+nt] += pick_map[ch]

    intensity = sliding_window_sum(hotmap, 5)
    return np.argmax(intensity)-max_sp, np.max(intensity)


class Gird_Searcher(object):
    def __init__(self, geometry, grid_lon, grid_lat, grid_dep,
                 model=None, filepath='./'):
        if isinstance(model, TauPyModel):
            self.model = model
            model = model.model
        elif isinstance(model, TauModel):
            self.model = TauPyModel()
            self.model.model = model
        else:
            model = TauModel.from_file(model)
            self.model = TauPyModel()
            self.model.model = model
        # model.serialize(os.path.join(filepath, 'model.npz'))

        if len(geometry[0]) == 2:
            geometry = np.insert(geometry, 2, values=0, axis=1).shape
        
        min_depth = min(min(grid_dep), geometry[:,2].min())
        if min_depth < 0 :
            self.depth_correction = -geometry[:,2].min()
            grid_dep += self.depth_correction
            geometry[:,2] += self.depth_correction
        else:
            self.depth_correction = 0
        np.save(os.path.join(filepath, 'geometry.npy'), geometry)
        self.geometry = geometry
        self.grid_lon = grid_lon
        self.grid_lat = grid_lat
        self.grid_dep = grid_dep
        self.nx, self.ny, self.nz = len(grid_lon), len(grid_lat), len(grid_dep)
        self.filepath = filepath

    def fit_map(self, pick_map, fs, n=5, mode='PS'):
        self.mode = mode
        self.intensity = np.zeros((self.nx, self.ny, self.nz))
        self.rel_time = np.zeros((self.nx, self.ny, self.nz))
        if n:
            self.n = n
            self.idx_lon = np.round(np.linspace(0, self.nx-1, n)).astype(int)
            self.idx_lat = np.round(np.linspace(0, self.ny-1, n)).astype(int)
            self.idx_dep = np.round(np.linspace(0, self.nz-1, n)).astype(int)
            rd = 1
            while len(self.idx_lon) + len(self.idx_lat) + len(self.idx_lon) > 9:
                print(f'Grid seaching... Round {rd}')
                self.calc_grid(pick_map, fs)
                self._update_index()
                rd += 1
            print(f'Grid seaching... Round {rd}')
            self.calc_grid(pick_map, fs)
        else:
            self.idx_lon = range(self.nx)
            self.idx_lat = range(self.ny)
            self.idx_dep = range(self.nz)
            self.calc_grid(pick_map, fs)
        idx = np.unravel_index(np.argmax(self.intensity), self.intensity.shape)
        self.loc_idx = idx
        return *self.ijk2lonlatdep(*idx), self.rel_time[idx]

    def calc_grid(self, pick_map, fs):
        for i in self.idx_lon:
            elo = self.grid_lon[i]
            for j in self.idx_lat:
                ela = self.grid_lat[j]
                for k in self.idx_dep:
                    edep = self.grid_dep[k]
                    if self.intensity[i, j, k] != 0:
                        continue
                    filename = os.path.join(self.filepath, f'{i}_{j}_{k}.npy')
                    if not os.path.exists(filename):
                        print(f'Calculating travel time for grid {i}, {j}, {k}.')
                        pyfile = Path(__file__).parent / 'calc_travel_time.py'
                        os.system(f'python {pyfile} {self.filepath} {elo} {ela} {edep} {i}_{j}_{k}.npy')

                    delay = np.load(filename)
                    delay = np.round(delay * fs).astype(int)
                    dsp, itst = calc_max(pick_map, delay, mode=self.mode)
                    self.intensity[i, j, k] = itst
                    self.rel_time[i, j, k] = dsp / fs

    def _update_index(self):
        idx = np.unravel_index(np.argmax(self.intensity), self.intensity.shape)
        ii = list(self.idx_lon).index(idx[0])
        s, e = self.idx_lon[max(ii-1, 0)], self.idx_lon[min(ii+1, len(self.idx_lon)-1)]
        self.idx_lon = self._new_idx(s, e)
        jj = list(self.idx_lat).index(idx[1])
        s, e = self.idx_lat[max(jj-1, 0)], self.idx_lat[min(jj+1, len(self.idx_lat)-1)]
        self.idx_lat = self._new_idx(s, e)
        kk = list(self.idx_dep).index(idx[2])
        s, e = self.idx_dep[max(kk-1, 0)], self.idx_dep[min(kk+1, len(self.idx_dep)-1)]
        self.idx_dep = self._new_idx(s, e)
        return self
    
    def _new_idx(self, s, e):
        n = e - s
        if n >= 4:
            return np.round(np.linspace(s, e, self.n)).astype(int)
        else:
            return list(range(s, e+1))

    def lonlatdep2ijk(self, lon, lat, dep):
        i = np.argmin(abs(self.grid_lon - lon))
        j = np.argmin(abs(self.grid_lat - lat))
        k = np.argmin(abs((self.grid_dep-self.depth_correction) - dep))
        return i, j, k

    def ijk2lonlatdep(self, i, j, k):
        return self.grid_lon[i], self.grid_lat[j], self.grid_dep[k]-self.depth_correction



def model_initialization(fname):

    """
    Load a custom model. It will create a '.npz' file if imput file is '.nd' or
    '.tvel'.
    """
    suffix = os.path.splitext(fname)[0]
    if not suffix[1] == '.npz':
        build_taup_model(fname, output_folder=suffix[0] + '.npz')
        fname = suffix[0] + '.npz'
        print(fname + ' created')

    model = TauPyModel()
    model.model = TauModel.from_file(fname)
    return model


def xy2deg(y1, x1, y2, x2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2) / 6371


def time_difference(elo, ela, edep, geometry, t_obs,
                    phase, model, coordsys='lonlat'):
    """
    Culculate the difference of observed arrival time and theoretical arrival
    time list of 1 grid point.
    """
    if coordsys == 'lonlat':
        coord2deg = locations2degrees
    elif coordsys == 'xy':
        coord2deg = xy2deg
    else:
        raise ValueError("Coordsys must be one of 'lonlat', 'xy'")
    stations = len(geometry)
    dt = t_obs
    for i in range(stations):
        deg = coord2deg(ela, elo, geometry[i, 1], geometry[i, 0])
        if phase[i] in ['p', 'P', 0]:
            phs = ['p', 'P']
        elif phase[i] in ['s', 'S', 1]:
            phs = ['s', 'S']
        else:
            raise ValueError("Phase must be 'P' or 'S'")
        arrivals = model.get_travel_times(source_depth_in_km=edep,
                                          receiver_depth_in_km=geometry[i, 2],
                                          distance_in_degree=deg,
                                          phase_list=phs)
        dt[i] -= arrivals[0].time
    return dt


def grid_search(lonlst, latlst, deplst, geometry, t_obs, phase, weight=None,
                model=TauPyModel(model='iasp91'), coordsys='lonlat',
                time_correction=True, norm_ord=1, parallel=True):
    """
    Grid search for 1 event
    """
    X, Y, Z = np.meshgrid(lonlst, latlst, deplst)
    grid = np.array([X.flatten(), Y.flatten(), Z.flatten()]).transpose()
    stations = len(geometry)
    if len(geometry[0]) == 2:
        geometry = np.concatenate((geometry, np.zeros((stations, 1))), axis=1)
    if parallel:
        cores = multiprocessing.cpu_count() - 1
        pool = multiprocessing.Pool(processes=cores)
        tasks = [[elo, ela, edep, geometry, t_obs, phase, model, coordsys] for
                 (elo, ela, edep) in grid]
        dt = pool.starmap(time_difference, tasks)
    else:
        dt = np.zeros((len(grid), stations))
        for i in tqdm(range(len(grid))):
            dt[i] = time_difference(grid[i, 0], grid[i, 1], grid[i, 2],
                                    geometry, t_obs, phase, model, coordsys)
    if not weight:
        weight = np.ones(len(geometry))
    if time_correction:
        if norm_ord == 1:
            dtau = np.median(dt, axis=0)
        elif norm_ord == 2:
            dtau = np.mean(dt, axis=0)
        else:
            raise ValueError("Order of the norm must be 'P' or 'S'")
        residual = np.linalg.norm(dt - dtau, ord=norm_ord, axis=0)
        pos = np.argmin(residual)
        elo, ela, edep = grid[pos]
        return [elo, ela, edep, residual[pos], dtau[pos]]
    else:
        residual = np.linalg.norm(dt, ord=norm_ord, axis=0)
        pos = np.argmin(residual)
        elo, ela, edep = grid[pos]
        return [elo, ela, edep, residual[pos]]
