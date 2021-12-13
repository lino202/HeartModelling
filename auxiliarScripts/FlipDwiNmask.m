close all; clear;
format long g;
addpath('functions','DTIEstimation');

% Read mask
mask = ReadNrrd('/home/mood/Desktop/002_control_pigs_Brav3/segmentations/basal2/medium_iso2_parts.seg.nrrd');
mask.pixelData = flip(mask.pixelData,2);

% Read original DWI image
dwidenoised  = ReadNrrd('/home/mood/Desktop/002_control_pigs_Brav3/nrrd_dwi/basal2/dwi_medium_iso2_denoised.nrrd');
dwidenoised.pixelData = flip(dwidenoised.pixelData,3);


WriteNrrdDwi('/home/mood/Desktop/002_control_pigs_Brav3/nrrd_dwi/basal2/dwi_medium_iso2_denoised_flipped.nrrd', dwidenoised);
WriteNrrdDwi('/home/mood/Desktop/002_control_pigs_Brav3/nrrd_dwi/basal2/medium_iso2_parts-flipped.seg.nrrd.nrrd', mask);



