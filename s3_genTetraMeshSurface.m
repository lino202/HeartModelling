% This code should be replace as well as the s3_genTetraMeshSurface
% when a docker image with ubuntu is used for tetgen. For now it uses
% WSL for using tetgen in linux that seems to generate better results
clear; close all; clc;
addpath('matlabFunctions', 'Libraries/iso2mesh-1.9.6');

% Input filenames
tetgenPath = '/home/maxi/Programs/tetgen1.6.0/tetgen';
dataPath   = 'D:/Paper3/Models/invivo/mi/cx/sample6_x/mesh/';
surfMesh   = append(dataPath, 'surfMesh.obj');
workdir    = append(dataPath, '');
outmesh    = append(workdir, 'tetmesh');

tetMaxVol = 0;
edgeLength = 0.3; %0.3 for paper3
wsl = 1;

% Read heart surface mesh and normalize normals
[snodes, sfaces, snormals] = ReadObj(surfMesh); %from Meshlab

regions=surfseeds(snodes(:,1:3),sfaces(:,1:3));
cmdopt = '-q1.414 -V';
tic
if tetMaxVol>0 && edgeLength<=0
    cmdopt = append(cmdopt, ' -a');
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

