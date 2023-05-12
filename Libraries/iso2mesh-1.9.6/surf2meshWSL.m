function surf2meshWSL(v,f,p0,p1,keepratio,maxvol,regions,holes,forcebox,method,cmdopt, outmesh, tetgenPath)
%
% [node,elem,face]=surf2mesh(v,f,p0,p1,keepratio,maxvol,regions,holes,forcebox)
%
% create quality volumetric mesh from isosurface patches
%
% author: Qianqian Fang, <q.fang at neu.edu>
% date: 2007/11/24
%
% input parameters:
%      v: input, isosurface node list, dimension (nn,3)
%         if v has 4 columns, the last column specifies mesh density near each node
%      f: input, isosurface face element list, dimension (be,3)
%      p0: input, coordinates of one corner of the bounding box, p0=[x0 y0 z0]
%      p1: input, coordinates of the other corner of the bounding box, p1=[x1 y1 z1]
%      keepratio: input, percentage of elements being kept after the simplification
%      maxvol: input, maximum tetrahedra element volume
%      regions: list of regions, specifying by an internal point for each region
%      holes: list of holes, similar to regions
%      forcebox: 1: add bounding box, 0: automatic
%
% outputs:
%      node: output, node coordinates of the tetrahedral mesh
%      elem: output, element list of the tetrahedral mesh
%      face: output, mesh surface element list of the tetrahedral mesh 
%             the last column denotes the boundary ID
%
% -- this function is part of iso2mesh toolbox (http://iso2mesh.sf.net)
%
fprintf(1,append('generating tetrahedral mesh from closed surfaces with WSL ', method, ' ...\n'));


if(keepratio>1 || keepratio<0)
   warn(['The "keepratio" parameter is required to be between 0 and 1. '...
         'Your input is out of this range. surf2mesh will not perform '...
	 'simplification. Please double check to correct this.']);
end

%Mesh resampling should be done before with meshlab
no=v;
el=f;

if(size(regions,2)>=4 && ~isempty(maxvol))
    warning('you specified both maxvol and the region based volume constraint,the maxvol setting will be ignored');
    maxvol=[];
end

dobbx=0;
if(nargin>=9)
	dobbx=forcebox;
end

% dump surface mesh to .poly file format
if(~iscell(el) && ~isempty(no) && ~isempty(el))
	saveoff(no(:,1:3),el(:,1:3),append(outmesh, '.off'));
end
deletemeshfile(append(outmesh, '.mtr'));
savesurfpoly(no,el,holes,regions,p0,p1,append(outmesh,'.poly'),dobbx);

% call tetgen to create volumetric mesh
deletemeshfile(append(outmesh,'.1.*'));
fprintf(1,'creating volumetric mesh from a surface mesh ...\n');


% This code is not working as for some reason I do not see wsl from matlab
% this is not worth to lose time with as docker container will be used in
% the future

% [status, cmdout]=system([cmdopt ' "' mwpath('post_vmesh.poly') '"']);
% disp(cmdout)
% if(status~=0)
%        error(sprintf('Tetgen command failed'));
% end
% read in the generated mesh
% [node,elem,face]=readtetgen(mwpath('post_vmesh.1'));
% fprintf(1,'volume mesh generation is complete\n');

tetgen = tetgenPath;
target = strrep(append(outmesh,'.poly'),'\','/');
target = strrep(target,'D:','/mnt/d');
cmd = append(tetgen, ' ', cmdopt, ' ', target, '\n');
fprintf(1,'Copy the following command in Ubuntu WSL using tetgen\n');
fprintf(1,cmd);

