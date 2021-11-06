close all; clear;
format long g;
addpath('functions','DTIEstimation');


dataPath = 'F:\DTI_konstas\data\sampleLE_MI1\';
dwiName = 'dwi_denoised.nrrd';                        % this must be a .nrrd 
mskName = 'segLabel.nrrd';
outputName = 'dti';


myo_flag = 1;
scar_flag = 2;
endo_flag = 3;
mid_flag = 4;
epi_flag = 5;

% Read mask
mask = ReadNrrd(append(dataPath, mskName));
mask = checkLPSOrientation(mask);

% Read original DWI image
dwidenoised  = ReadNrrd(append(dataPath, dwiName));
dwidenoised = checkLPSOrientation(dwidenoised);
DWI = double(dwidenoised.pixelData);

checkSpaceOriDir(mask, dwidenoised);

% Extract gradients
grads = ExtractDwiGrads(dwidenoised.metaData);

% Set b-value for gradients and DTI order (standard is 2)
dti_order = 2;
bval = str2num(dwidenoised.metaData.DWMRI_b_value);
b_values = bval*ones(size(grads,1),1);

if grads(1,:) == [0,0,0]
    grads = grads(2:end,:);
    b_values = b_values(2:end);
    S0vol = DWI(1,:,:,:);
    DWIvol = DWI(2:end,:,:,:);
end

% Construct all possible monomials for the specific DTI order
% Computes G from section 5.1 (ISBI'10)
G = constructMatrixOfMonomials(grads, dti_order);

% Construct set of polynomial coefficients C
% Computes C from section 5.1 (ISBI'10)
C = constructSetOf321Polynomials(dti_order)'; 
P = G*C;
P = -diag(b_values)*P;

% Compute DTI image
dti_size = size(DWI); dti_size(1) = 6;
DTI = zeros(dti_size);

start_time=cputime;
for k=1:dti_size(4)
    for j=1:dti_size(3)
        for i=1:dti_size(2)
            % Gradient values at the voxel
            DWIvox = DWIvol(:,i,j,k);
            S0vox = S0vol(:,i,j,k);
            
            if (sum(DWIvox) ~= 0)
                % DTI computation
                DWIvox(DWIvox==0)=0.1;
                y = log(DWIvox/S0vox);
                
                x = lsqnonneg(P, y);

             
                unique_coeffs = C*x;
                
                % final tensor values d11 d12 d13 d22 d23 d33
                d = [unique_coeffs(6); unique_coeffs(5)/2; unique_coeffs(4)/2;
                     unique_coeffs(3); unique_coeffs(2)/2; unique_coeffs(1)];
                 
                 DTI(:,i,j,k) = d;
            end
        end
    end
end
end_time=cputime;
fprintf(1,'\nTotal estimation time: %.0f ms\n\n',(end_time-start_time)*1000);

%% Convert DTI image to point cloud with fiber vectors 
% Get ijk2Points transform matrix
origin = textscan(mask.metaData.space_origin,'(%f,%f,%f)');
origin = cell2mat(origin);
%Use the mask ijktoLPS as directions are unchanged but readd original
%origin as it has been change for not indexing form 0
ijk2Points = mask.ijkToLpsTransform;
ijk2Points(:,4) =  [origin(1);origin(2);origin(3);1];

[nX,nY,nZ] = size(mask.pixelData);
part_flag = zeros(nX*nY*nZ,1);
fibs = zeros(nX*nY*nZ,3);
points = zeros(nX*nY*nZ,3);              %Spatial
pointVoxelMap = zeros(nX*nY*nZ,3);       %IJK
id = 1;
for k=1:nZ
    for j=1:nY
        for i=1:nX
            if(mask.pixelData(i,j,k)~=0)
                
                % Convert voxel to physical point
                ijk = [(i-1);(j-1);(k-1);1];
                xyz = (ijk2Points * ijk)';
                points(id,:) = xyz(1:3);
                
                pointVoxelMap(id,:) = [i,j,k];
                
                % d11 d12 d13 d22 d23 d33
                d = DTI(:,i,j,k);
                d11 = d(1); d12 = d(2); d13 = d(3);
                d22 = d(4); d23 = d(5); d33 = d(6);

                D = [d11, d12, d13;
                     d12, d22, d23;
                     d13, d23, d33];
                
                % Find max eigen value
                [v,d] = eig(D);
                [~,maxd_id] = max(diag(d));
                
                % Get principal direction of diffusion tensor
                fibs(id,:) = v(:,maxd_id)';
                
                % Set partition id of the point
                part_flag(id) = mask.pixelData(i,j,k);
                
                id=id+1;

            end
        end
    end
end


points(~any(points,2), :) = [];
part_flag(~any(part_flag,2), :) = [];
pointVoxelMap(~any(pointVoxelMap,2), :) = [];
fibs(~any(fibs,2), :) = [];

% Make partition group nodes
endo_nodes = find(part_flag==endo_flag);
mid_nodes = find(part_flag==mid_flag);
epi_nodes = find(part_flag==epi_flag);
myo_nodes = find(part_flag==myo_flag);
scar_nodes = find(part_flag==scar_flag);

% Make partition field data
endo_fd = zeros(size(points,1),1);
endo_fd(endo_nodes) = 1;

mid_fd = zeros(size(points,1),1);
mid_fd(mid_nodes) = 1;

epi_fd = zeros(size(points,1),1);
epi_fd(epi_nodes) = 1;

myo_fd = zeros(size(points,1),1);
myo_fd(myo_nodes) = 1;

scar_fd = zeros(size(points,1),1);
scar_fd(scar_nodes) = 1;

allparts_fd = zeros(size(points,1),1);
allparts_fd(endo_nodes) = endo_flag;
allparts_fd(mid_nodes) = mid_flag;
allparts_fd(epi_nodes) = epi_flag;
allparts_fd(myo_nodes) = myo_flag;
allparts_fd(scar_nodes) = scar_flag;


% Report partition percentages
fprintf('endo: %f %%\n',100*(length(endo_nodes)/length(points)));
fprintf('mid: %f %%\n',100*(length(mid_nodes)/length(points)));
fprintf('epi: %f %%\n',100*(length(epi_nodes)/length(points)));
fprintf('myo: %f %%\n',100*(length(myo_nodes)/length(points)));
fprintf('scar: %f %%\n',100*(length(scar_nodes)/length(points)));

save(append(dataPath, 'pointVoxelMap'),'pointVoxelMap');

% Output of dti points and fibers
field_data = {{endo_fd,'endo_nodes'},...
              {mid_fd,'mid_nodes'},...
              {epi_fd,'epi_nodes'},...
              {myo_fd,'myo_nodes'},...
              {scar_fd,'scar_nodes'},...
              {allparts_fd,'all_parts'},...
              {fibs,'dti-fibers'}};
SavePointsToVtk(append(dataPath, outputName, '.vtk'), points, field_data);




