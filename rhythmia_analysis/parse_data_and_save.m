%%%
% 
% Code for getting the anatomy, maps on mesh, surfaceElectrodes and beats
% 
%%%

% This code parses the study and functions in python are used to compute meshes and
% point clouds for high-quality 3D visualization in paraview. Also the study parsing
% allows to use the openep matlab function which are not yet fully implemented in python
% This parsing also eases the python reading and parsing with h5py
% the name of the catheter and other names and the tags in surfaceElectrodes are not parsed
% as the catheter usually is always Orion in the whole study and the tags depend on the case,
% also some other reference signals might be in the file so first control all the data is 
% useful is parsed accordingly



clear all
clc

tic
base_path  = '/home/maxi/Documents/PhD/Paper3/Study_2023_09_11_03-39';
input_path = append(base_path, '/map2_LV_.mat');
out_path   = append(base_path, '/results/map2');
file_anatomy = append(out_path, '/anatomy.mat');
file_maps  = append(out_path, '/maps.mat');
file_se    = append(out_path, '/surfaceElectrodes.mat');
file_beats = append(out_path, '/beats.mat');
load(input_path);

if ~exist(out_path, 'dir')
    mkdir(out_path)
end

%% Get the anatomy
points = data.anatomy.vertices_mm';
cells  = data.anatomy.faces;

save(file_anatomy, "points", "cells");

%% Get maps

maps_voltage_bi     = data.maps.voltage.bipolar_mV;
maps_voltage_uni    = data.maps.voltage.unipolar_mV;
maps_activation_bi  = data.maps.activation.bipolar_ms;
maps_activation_uni = data.maps.activation.unipolar_ms;
maps_cutoutmask     = data.maps.cutoutMask;

save(file_maps, "maps_voltage_uni", "maps_voltage_bi", "maps_activation_uni", "maps_activation_bi", "maps_cutoutmask");

%% Get surfaceElectrodes
sampleFreq         = data.sampleFrequency_Hz;
nSurfaceElectrodes = length(data.surfaceElectrodes);
se_location        = zeros(nSurfaceElectrodes, 3);
se_activation_uni  = zeros(1,nSurfaceElectrodes);
se_activation_bi   = zeros(1,nSurfaceElectrodes);
se_projected_dist  = zeros(1,nSurfaceElectrodes);
se_voltage_uni  = zeros(1,nSurfaceElectrodes);
se_voltage_bi   = zeros(1,nSurfaceElectrodes);
se_electrode_uni  = zeros(1,nSurfaceElectrodes);
se_electrode_bi   = zeros(1,nSurfaceElectrodes);
se_beat           = zeros(1,nSurfaceElectrodes);

se_mappingsigs_nsamples = length(data.surfaceElectrodes(1).mappingSignals.bipolar.samples_mV);
se_mappingsigs_bipolar = zeros(nSurfaceElectrodes,se_mappingsigs_nsamples);
se_mappingsigs_unipolar = zeros(nSurfaceElectrodes,se_mappingsigs_nsamples);

for i = 1:nSurfaceElectrodes
    se_location(i,:)     = data.surfaceElectrodes(i).surfaceLocation_mm';
    se_projected_dist(i) = data.surfaceElectrodes(i).projectedDistance_mm;
    se_activation_uni(i) = data.surfaceElectrodes(i).activation.unipolar_ms;
    se_activation_bi(i)  = data.surfaceElectrodes(i).activation.bipolar_ms;
    se_voltage_uni(i)    = data.surfaceElectrodes(i).voltage.unipolar_mV;
    se_voltage_bi(i)     = data.surfaceElectrodes(i).voltage.bipolar_mV;
    se_electrode_uni(i)  = data.surfaceElectrodes(i).electrode.unipolar;
    se_electrode_bi(i)   = data.surfaceElectrodes(i).electrode.bipolar;
    se_beat(i)           = data.surfaceElectrodes(i).beat;

    se_mappingsigs_bipolar(i,:)=data.surfaceElectrodes(i).mappingSignals.bipolar.samples_mV';
    se_mappingsigs_unipolar(i,:)=data.surfaceElectrodes(i).mappingSignals.unipolar.samples_mV';
end

save(file_se, "sampleFreq", "se_location", "se_projected_dist", ...
    "se_activation_uni", "se_activation_bi", "se_voltage_uni", ...
    "se_voltage_bi", "se_electrode_uni", "se_electrode_bi", "se_beat", ...
    "se_mappingsigs_unipolar", "se_mappingsigs_bipolar");

%% Get beats
nBeats = length(data.beats);
be_mapsetts_win_firstsample  = zeros(1,nBeats);
be_mapsetts_win_lastsample   = zeros(1,nBeats);
be_mapsetts_win_timrefsample = zeros(1,nBeats);
be_number = zeros(1,nBeats);
be_time_s = zeros(1,nBeats);

be_ecg_nSamplesPerSignal = size(data.beats(1).referenceSignals.ECG.unipolar.samples_mV, 1);
be_ecg_nSignals          = size(data.beats(1).referenceSignals.ECG.unipolar.samples_mV, 2);
be_ecg_uni_samples       = zeros(nBeats, be_ecg_nSamplesPerSignal, be_ecg_nSignals);
be_ecg_uni_channels      = cell(nBeats, be_ecg_nSignals);

be_mapsigs_nSamplesPerSignal = size(data.beats(1).mappingSignals.bipolar.samples_mV, 1);
be_mapsigs_nChannels_uni     = size(data.beats(1).mappingSignals.unipolar.samples_mV, 2); %64 with orion catheter (8 electrodes in 8 blades)
be_mapsigs_nChannels_bi      = size(data.beats(1).mappingSignals.bipolar.samples_mV, 2);  %56 with orion catheter (7 pair of electrodes in every if the 8 blades)
be_mapsigs_bi_samples   = zeros(nBeats, be_mapsigs_nSamplesPerSignal, be_mapsigs_nChannels_bi);
be_mapsigs_uni_samples  = zeros(nBeats, be_mapsigs_nSamplesPerSignal, be_mapsigs_nChannels_uni);
be_mapsigs_uni_channels = cell(nBeats, be_mapsigs_nChannels_uni);
be_mapsigs_bi_channels  = cell(nBeats, be_mapsigs_nChannels_bi);
be_mapsigs_uni_location = zeros(nBeats, be_mapsigs_nChannels_uni, 3);
be_mapsigs_bi_location  = zeros(nBeats, be_mapsigs_nChannels_bi, 3);

for i = 1:nBeats
    be_mapsetts_win_firstsample(i)  = data.beats(i).mappingSettings.window.firstSample;
    be_mapsetts_win_lastsample(i)   = data.beats(i).mappingSettings.window.lastSample;
    be_mapsetts_win_timrefsample(i) = data.beats(i).mappingSettings.window.timingReferenceSample;
    
    be_ecg_uni_samples(i,:,:) = data.beats(i).referenceSignals.ECG.unipolar.samples_mV;
    be_ecg_uni_channels(i,:)= data.beats(i).referenceSignals.ECG.unipolar.channels;
    
    be_mapsigs_uni_samples(i,:,:) = data.beats(i).mappingSignals.unipolar.samples_mV;
    be_mapsigs_bi_samples(i,:,:)  = data.beats(i).mappingSignals.bipolar.samples_mV;
    be_mapsigs_uni_channels(i,:) = data.beats(i).mappingSignals.unipolar.channels;
    be_mapsigs_bi_channels(i,:)  = data.beats(i).mappingSignals.bipolar.channels;
    be_mapsigs_uni_location(i,:,:) = data.beats(i).mappingSignals.unipolar.location_mm';
    be_mapsigs_bi_location(i,:,:)  = data.beats(i).mappingSignals.bipolar.location_mm';
    
    be_number(i)    = data.beats(i).number;
    be_time_s(i) = data.beats(i).time_s;
end

save(file_beats, "sampleFreq", "be_mapsetts_win_firstsample", "be_mapsetts_win_lastsample", ...
    "be_mapsetts_win_timrefsample", "be_ecg_uni_samples", "be_ecg_uni_channels", ...
    "be_mapsigs_uni_samples", "be_mapsigs_bi_samples", "be_mapsigs_uni_channels", "be_mapsigs_bi_channels", ...
    "be_mapsigs_uni_location", "be_mapsigs_bi_location", "be_number", "be_time_s");

toc







    






