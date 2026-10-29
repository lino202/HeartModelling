% This code should be replace as well as the s3_genTetraMeshSurface
% when a docker image with ubuntu is used for tetgen. For now it uses
% WSL for using tetgen in linux that seems to generate better results

%It creates the .ply and .mrt file to use in Tetgen. When giving the edge
%length, it creates the .mtr file to use there.
%At the end, it also creates the line to be used to run tetgen

clear; close all; clc;
addpath('matlabFunctions', 'Libraries/iso2mesh-1.9.6');

% Input filenames
% tetgenPath = '/home/maxi/Programs/tetgen1.6.0/tetgen';
tetgenPath = '/home/jrdzc16/Simulations/tetgen1.6.0/tetgen';  %JRDZC Modify 20/01/2025
% tetgenPath = '/home/jrdzc16/Simulations/TetGen-1.5.1/tetgen';  %JRDZC Modify 12/09/2025 
% dataPath   = '/home/maxi/Documents/PhD/Paper3/he/sample3/mesh/';
% dataPath   = 'E:/Jimena/HCULB/IHD/Segmentations/MI_MRI_32/mesh/'; %JRDZC Modify 20/01/2025

dataPath = 'E:/Jimena/HCULB/IHD/Segmentations/cube/mesh/' ;
% surfMesh   = append(dataPath, 'surfMesh.obj');
surfMesh   = append(dataPath, 'surface_mesh_orig_remesh.obj');  %JRDZC Modify 20/01/2025
workdir    = append(dataPath, '');
outmesh    = append(workdir, 'tetmesh');

tetMaxVol = 0;
edgeLength = 0.32; %0.32 for opencarp
wsl = 1;

% -a Applies a maximum tetrahedron volume constraint.
% -k Outputs mesh to .vtk file for viewing by Paraview
% -m Applies a mesh sizing function.
% The -m switch is used in mesh refinement, i.e., together with the -q switch. 
% It applies a user-defined mesh sizing function which specifies the desired edge lengths 
% in the final mesh. It aims to create an adaptive mesh whose edge lengths are conforming to this function.
% At the moment, only isotropic mesh sizing functions are supported.
% -V Adding a -V switch in the command line, TetGen will print a mesh quality report
% (aspect ratios, radius-edge ratios, dihedral angles) of the
% generated tetrahedral mesh on the screen


% Read heart surface mesh and normalize normals
%[snodes, sfaces, snormals] = ReadObj(surfMesh); %from Meshlab
[snodes, sfaces, snormals] = ReadObj(surfMesh); %from Meshlab %JRDZC 28/02/2025

regions=surfseeds(snodes(:,1:3),sfaces(:,1:3));

%Add volume constraint
volTet=(edgeLength^3)/(6*sqrt(2));

% calculate a set of interior points with each enclosed by a closed
% component of a surface
cmdopt = '-p -q1.414 -V -D'; %New version Maxi 03/2025
% cmdopt = strcat('-p -q1.414 -V -D -a',num2str(volTet)); %New version Maxi 03/2025 + vol constraint JRDZC 11/09/2025
% cmdopt = '-q1.414 -V';
tic
if tetMaxVol>0 && edgeLength<=0
%     cmdopt = append(cmdopt, ' -a');
    cmdopt = append(cmdopt, ' -a', num2str(tetMaxVol)); %maxi modified 2025
    if wsl
        cmdopt = append(cmdopt, ' -k');
        surf2meshWSL(snodes,sfaces,[],[],1,tetMaxVol,regions,[], 0, 'tetgen', cmdopt, outmesh, tetgenPath);
    else
        [nodes,elems,faces]=surf2mesh(snodes,sfaces,[],[],1,tetMaxVol,regions,[], 0, 'tetgen', cmdopt);
        elems=removedupelem(elems);
    end
elseif edgeLength>0 && tetMaxVol<=0
    snodes = [snodes, ones(size(snodes,1),1) * edgeLength];
    cmdopt = append(cmdopt, ' -m');
    if wsl
        cmdopt = append(cmdopt, ' -k');
        surf2meshWSL(snodes,sfaces,[],[],1,[],regions,[],0, 'tetgen', cmdopt, outmesh, tetgenPath);
    else
        [nodes,elems,faces]=surf2mesh(snodes,sfaces,[],[],1,[],regions,[],0, 'tetgen', cmdopt);
        elems=removedupelem(elems);
    end  
else
    error("Select correctly edgelength or maxVol")
end
toc


% visualize the resulting mesh
% plotmesh(nodes,faces(:,1:3));
% axis equal;

% figure; hold on; 
% ShowFaces(nodes,faces(:,1:3),[.8 .8 .8],0.4);
% plot3(nodes(:,1),nodes(:,2),nodes(:,3),'bo','MarkerFaceColor','b','MarkerSize',5)
% hold off; daspect([1 1 1]);
if ~wsl
    tic
    SaveTetVtk(vtk_output, nodes, elems(:,1:4), [], [], []);
    toc
end

%% -----------------------------------------------------------------


%/mnt/c/Maxi/Programs/tetgen1.6.0/tetgen -pq1.2/30 -D -m -V -k -o/120 -O 2/7/9 /mnt/e/HeartModelling/Data_1/sampleLE_Control2/invivo/F19_Nico/cover/mi_smooth/mesh/tetmesh_new.poly


