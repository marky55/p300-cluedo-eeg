# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 14:03:18 2019
Revised on Wed Aug 24 10:17:00 2022

@author: Bob Van Dyck
"""

import os
import numpy as np
import scipy.io 
import matplotlib.pyplot as plt

class Dataclass():
    
    def __init__(self, matfile='data/Cluedo1.mat'):
        mat = scipy.io.loadmat(matfile)
        self.channelnames= [name.item() for name in mat["channelNames"][0]]
        self.data = mat["EEG"]
        self.markers = mat["markers"].flatten() 
        self.samplerate = mat["sampleRate"].item()

def get_timestamps(markers, samplerate, epoch_time=1.0, preepoch_time=0.1):
    timestamps = []
    for onset, marker in enumerate(markers):
        if marker != 0:
            start = onset - preepoch_time * samplerate
            end = onset + epoch_time * samplerate
            timestap = [marker, start, onset, end]
            timestamps.append(timestap)
    
    return np.array(timestamps)

def subtract_baseline(data, timestamps, n_channels, epoch_time, samplerate):
    n_epochs = len(timestamps)
    epochs = np.ndarray([n_epochs, n_channels, int(samplerate * epoch_time)]) 
    for i, timestamp in enumerate(timestamps):
        start, onset, end = timestamp[1:].astype(int)
        baseline = np.mean(data[:, start:onset], axis=-1)
        epochs[i] = np.subtract(data[:, onset:end], baseline[:, np.newaxis])
                
    return epochs
    
def mean_per_marker(epochs, timestamps, marker_set):
    markers = timestamps[:,0]
    epochs_per_marker = {marker:[] for marker in marker_set}
    mean_epochs_per_marker = {marker:[] for marker in marker_set}
    for marker, epoch in zip(markers, epochs):  
        epochs_per_marker[marker].append(epoch)
    for marker, epochs in epochs_per_marker.items():
        mean_epochs_per_marker[marker] = np.mean(epochs, axis=0)
 
    return mean_epochs_per_marker

# def main():
    
# load data 
EEG = Dataclass('data/Cluedo1.mat')
data = EEG.data
markers = EEG.markers
channelnames = EEG.channelnames
samplerate = EEG.samplerate 

# channel selection
channels = ['Fz'] #, 'Cz', 'CP1', 'CP2', 'Pz', 'PO3', 'PO4']
delete = [i for i, name in enumerate(channelnames) if name not in channels]
data = np.delete(data, delete, axis=0)

# inspect data
n_channels, n_samples = data.shape
print(f"channels x samples: {data.shape}")
marker_set = set(markers)

# get timestamps, subtract baseline, epoching
timestamps = get_timestamps(markers, samplerate, 1.0, 0.1) 
epochs = subtract_baseline(data, timestamps, n_channels, samplerate, 1.0)
mean_epoch_per_marker = mean_per_marker(epochs, timestamps, marker_set)

# legend: suspects/weapons/locations
suspects = ['Brown', 'Mustard', 'Peach', 'Scarlett', 'Grey', 'Peacock', 'White', 'Plum', 'Green']
suspects_marker = np.arange(11,20)
weapons = ['Axe', 'Blunderbuss', 'Candlestick', 'Dagger', 'Lead Pipe', 'Poison', 'Revolver', 'Rope', 'Spanner']
weapons_marker = np.arange(21,30)
locations = ['Ballroom', 'Billiard', 'Conservatory', 'Dining', 'Hall', 'Kitchen', 'Library', 'Lounge', 'Study']
locations_marker = np.arange(31,40)

# group per suspects/weapons/locations
# compute mean epoch (mean over different repetitions of the same suspect/weapon/location)
mean_epoch_suspects = np.stack([mean_epoch for marker, mean_epoch in mean_epoch_per_marker.items()
                                if marker in suspects_marker])

mean_epoch_weapons = np.stack([mean_epoch for marker, mean_epoch in mean_epoch_per_marker.items()
                              if marker in weapons_marker])

mean_epoch_locations = np.stack([mean_epoch for marker, mean_epoch in mean_epoch_per_marker.items()
                              if marker in locations_marker])

## Visual method

# plot: suspects
for electrode in range(len(channels)):
    plt.figure(electrode)
    plt.plot(mean_epoch_suspects.T[:, electrode])
    plt.legend(suspects)
    plt.title("Mean epoch (ERP) per suspect")
    plt.show()

# plot: weapons
for electrode in range(len(channels)):
    plt.figure(electrode)
    plt.plot(mean_epoch_weapons.T[:, electrode])
    plt.legend(weapons)
    plt.title("Mean epoch (ERP) per weapon")
    plt.show()
    
# plot: locations
for electrode in range(len(channels)):
    plt.figure(electrode)
    plt.plot(mean_epoch_locations.T[:, electrode])
    plt.legend(locations)
    plt.title("Mean epoch (ERP) per location")
    plt.show()

## Peak based methods

# peak values
peak_suspects = np.max(mean_epoch_suspects, axis=2)
peak_weapons = np.max(mean_epoch_weapons, axis=2)
peak_locations = np.max(mean_epoch_locations, axis=2)

# mean peak over electordes
mean_peak_suspects = np.mean(peak_suspects, axis=1)
mean_peak_weapons =  np.mean(peak_weapons, axis=1)
mean_peak_locations =  np.mean(peak_locations, axis=1)
suspect = np.argmax(mean_peak_suspects)
weapon = np.argmax(mean_peak_weapons)
location = np.argmax(mean_peak_locations)

print("Method: mean peak over electrodes:")
print(f"{suspects[suspect]} killed with the {weapons[weapon]} in the {locations[location]}")

# electrode voting
votes_suspects = np.argmax(peak_suspects, axis=0)
votes_weapons =  np.argmax(peak_weapons, axis=0)
votes_locations =  np.argmax(peak_locations, axis=0)
suspect = np.argmax(np.bincount(votes_suspects))
weapon = np.argmax(np.bincount(votes_weapons))
location = np.argmax(np.bincount(votes_locations))

print("Method: peak-based voting over electrodes:")
print(f"{suspects[suspect]} killed with the {weapons[weapon]} in the {locations[location]}")
