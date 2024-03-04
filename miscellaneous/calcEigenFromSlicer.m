close all; clear;
format long g;
addpath('../matlabFunctions','../libraries/DTIEstimation');


dataPath = 'D:/Paper3/DWI/mi/sample8/';
dtiName = 'dti.nrrd';                        % this must be a .nrrd 
mskName = 'label_biv.nrrd';
outputName = 'main_eigen';


myo_flag = 1;
scar_flag = 2;
endo_flag = 3;
mid_flag = 4;
epi_flag = 5;

% Read mask
mask = ReadNrrd(append(dataPath, mskName));
mask = checkLPSOrientation(mask);

% Read original DWI image
dti  = ReadNrrd(append(dataPath, dtiName));
dti = checkLPSOrientation(dti);
DTI = double(dti.pixelData);

checkSpaceOriDir(mask, dti);

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
                
                
                d = DTI(:,i,j,k);

                D = [d(1), d(2), d(3);
                     d(4), d(5), d(6);
                     d(7), d(8), d(9)];
                
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
              {fibs,'dti_fibers'}};
SavePointsToVtk(append(dataPath, outputName, '.vtk'), points, field_data);




