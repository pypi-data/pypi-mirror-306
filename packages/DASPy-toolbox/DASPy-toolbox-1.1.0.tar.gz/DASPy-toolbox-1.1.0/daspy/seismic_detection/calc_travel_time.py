import sys
import os
import multiprocessing
import numpy as np
from obspy.taup.tau_model import TauModel
from obspy.taup import TauPyModel
from daspy.seismic_detection.location import calc_travel_time


cores = multiprocessing.cpu_count() - 1
pool = multiprocessing.Pool(processes=cores)


filepath, elo, ela, edep, savefile = sys.argv[1:6]

elo, ela, edep = map(float, (elo, ela, edep))
model = TauPyModel()
model.model = TauModel.from_file(os.path.join(filepath, 'model.npz'))
geometry = np.load(os.path.join(filepath, 'geometry.npy'))
tasks = [(model, elo, ela, edep, *geo) for geo in geometry]
delay = pool.starmap(calc_travel_time, tasks)
delay = np.array(delay)
np.save(os.path.join(filepath, savefile), delay)