close all; clear;
format long g;
addpath('matlabFunctions','libraries/LMMSEDWI','libraries/MRNoiseEstimators','libraries/MRNoiseEstimators/localstat','libraries/DTIEstimation');


dataPath = 'D:/Paper3/DWI/sample1_bis/';
dwiName = 'dwi_reg_DTI_medium.nrrd';                        % this must be a .nrrd 
mskName = 'Segmentation.seg.nrrd';
outputName = 'dwi_denoised_lmmsedwi.nrrd';


% Read original DWI image
dwi  = ReadNrrd(append(dataPath, dwiName));
dwi = checkLPSOrientation(dwi);

% Read mask
mask = ReadNrrd(append(dataPath, mskName));
mask = checkLPSOrientation(mask);


checkSpaceOriDir(mask, dwi);



DWInoisy = double(dwi.pixelData);
DWInoisy = permute(DWInoisy,[3,2,4,1]);

maskImage = logical(mask.pixelData);
maskImage = permute(maskImage,[2,1,3]);


% Extract gradients
grads = ExtractDwiGrads(dwi.metaData);

% Compute noise
sigmas = zeros(size(DWInoisy,4),1);
for n=1:size(DWInoisy,4)
    sigmas(n)=AjaNE3D(DWInoisy(:,:,:,n),20,80,3);
end
sigma = max(sigmas);

% Denoise DWI image
tic;
NG = 5; rs = [2;2;2]; rc = [1;1;1];
DWIfilter = jaLMMSEDWI(DWInoisy,grads,sigma,'rs',rs,'rc',rc,'beta',1.5,'Ng',NG,'onlyUNLM',false,'filterOutliers',true,'mask', maskImage);
etime = toc;
disp(['Whole Wiener version with mask and all gradients completed in ',num2str(etime),' seconds']);

% Show denoising result
slice = 46; g = 3;
figure(1); subplot(1,2,1);
imshow(DWInoisy(:,:,slice,g),[]);
title('Original noisy slice');

subplot(1,2,2);
imshow(DWIfilter(:,:,slice,g),[]);
title('Whole filter mixing all gradients');

DWIfilter = permute(DWIfilter,[4,2,1,3]);
dwi.pixelData = int16(DWIfilter);
WriteNrrdDwi(append(dataPath,outputName ), dwi);



