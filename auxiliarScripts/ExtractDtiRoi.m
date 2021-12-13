close all; clear;
format long g;
addpath('functions');

dwi  = ReadNrrd('/home/mood/Desktop/002_control_pigs_Brav3/nrrd_dwi/basal2/dwi_medium_iso2.nrrd');
dti  = ReadNrrd('/home/mood/Desktop/002_control_pigs_Brav3/nrrd_dwi/basal2/dti_medium_iso2.nrrd');
mask = ReadNrrd('/home/mood/Desktop/002_control_pigs_Brav3/segmentations/basal2/medium_iso2_labels.seg.nrrd');

% Convert mask to mhd label
WriteMhd('/home/mood/Desktop/002_control_pigs_Brav3/segmentations/basal2/medium_iso2-label.mhd',mask);

% Delete DTI data out of mask
[nX,nY,nZ] = size(mask.pixelData);
nnZ = nX*nY*nZ;
for k=1:nZ
    for j=1:nY
        for i=1:nX
            if(mask.pixelData(i,j,k)==0)
                dwi.pixelData(:,i,j,k) = 0;
                dti.pixelData(:,i,j,k) = 0;
                nnZ = nnZ-1;
            end
        end
    end
end

% Save cropped mask
WriteNrrdDwi('/home/mood/Desktop/002_control_pigs_Brav3/nrrd_dwi/basal2/dwi_medium_iso2_cropped.nrrd', dwi);
WriteNrrdDti('/home/mood/Desktop/002_control_pigs_Brav3/nrrd_dwi/basal2/dti_medium_iso2_cropped.nrrd', dti);

