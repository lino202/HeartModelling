# HeartPatch

## Intro
We generally start with a scaffold shell and/or x_scaffold. 

The scaffold_shell is the tetrahedrical mesh of the volumen of the patch and the quad is the shell type mesh of the actual scaffold of the patch
with the pores having any size or shape. We aligned those to the heart mesh where we want to project and finally we label the contact zone and corners in one face of the scaffold mesh (shell or X_).

## Getting landmarks on the heart

With this we use s1_getInitialLMs.py scripts which loads the heart mesh and compute the points in the mesh of the heart that correspond to the projection of the ones that are contacting nodes in the scaffold mesh.
We have seen that using all nodes in the contact zone/face gives better results. We also can use a meshHeart just a piece of the epicardium to which we are going to connect, is not necessary to have all superfical epicardial
mesh. You can make this piece of heart epicardium filled with more triangles (really refined) to better precision.

## Generating the inp file for Abaqus

Then this code makes the inp file for from the Abaqus command line launch the deformation. Take into account the deformation cannot be a alot so somew parts of the patch can go inside the epi mesh 
in order to allow a smaller deformation in other parts. For exmaple the patch centre go inside the epi mesh in order to put the corners nearer to the epi mesh and allow smaller deformations and not have a really small 
deformation in the centre and huge in the corners which will not finish in the desired positions.

```
{
            "name": "s2_createInpModel",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/heartPatch/s2_createInpModel.py",
            "console": "integratedTerminal",
            "args": [
                "--meshHeart",        "/mnt/d/Paper4/Models/sample4/EHT/epi_refine.obj",
                "--meshOnHeart",      "/mnt/d/Paper4/Models/sample4/EHT/epi_refine_lms.vtk",
                "--meshScaffold",     "/mnt/d/Paper4/Models/sample4/EHT/scaffolds/scaffold_shell_lms.vtk",
                "--outPath",          "/mnt/d/Paper4/Models/sample4/EHT/l1_eht_projection.inp",
                "--heartSurface",
                // "--scaffoldSurface",
            ] 
        },
```

Also we are using now only the scaffold shell and not the x_scaffold so the comment on param scaffoldSurface signals that we are using a volumetric mesh and no the surface mesh made of quads that is x_scaffold

## Projection / Embedding

After cleanning the mesh and smoothing maybe its vertices we can project/embed it into the heart with a script (s4 as 03_03_2025)


## Xor mesh generation and cleanning inner EHT/Patch

We generate the xor on meshlab with Filters -> Remeshing -> Mesh Boolean ... (XOR)

Once you have the xor (and previously or not of the cleanning of the triangles of the interface) we erase the tris in the inner of the heart
that were part of the patch. For this we need a surf_xor.ply mesh where the faces of the patch were added with a color in meshlab previous the xor 
So we add both meshes in meshlab and add to the mesh scaffold a color with Filters -> Color Creation -> Per Face Color Function and select a RED patch. 
For the meshHeart you can also add a color but it does not have to have the red component on 255 (see code s5_genMIPatchSurfFromXor).
Then we apply the xor an set the transfer face color to true and save this xor mesh as .ply. When saving the .ply we need to uncheck byte encoding (and check color of course!) 
as it gives an error when reading with meshio.

Moreover, the meshHeart and meshPatch in s5_genMIPatchSurfFromXor should be the exact mesh of the xor without the patch or the heart, respectively. You can obtain this from the xor mesh
using  on meshlab Filters -> Selection -> Conditional Face Selection and putting fr == 255 for the patch and deleting all vertexs and faces. Then you can recompute the normals
with Filters -> Normals .. -> Recompute normals coherently and when the shades of the heart/patch meshes are correct you export them and it is done :P

## Xor mesh cleanning of irregular tris

Initially we have the file final_mipatch_surfmesh.obj which is the patch+heart with irregular tris in the interface. With this file we use the sscript s6_distinguishPatchHeart.py
for generating a final_mipatch_surfmesh.ply or .obj which has colors. Red is the patch nodes and black the heart nodes. From here we use this final heart_patch mesh for cleaning the interface with meshlab and blender 
so the node identification is preseerved after cleaning and we can use it on s7_genTetMI_EHT for giving the desired edge_length per node.

So, with this mesh we can Filters -> Selection -> select problematic faces with the aspect ratio on meshlab, grow the selection and filter with the isotropic remeshing filter to repair the interface
Some elongated tris can be repair manually using blender in edit mode and by deleting vertices and filling with tris (pressing F when two or tree vertexs are selected for generating an edge or a triangle).
In blender for seeing the vertex/node color, in the top/right corner of the VIEWPORT (not the entire screen) you have a dropdown which says viewport shading and you can select attribute for seeing the red nodes 
of the patchs and black nodes of the heart. Then, you save this mesh in .obj is not necessary that the normals are ok but we aware of this when seeing the mesh in meshlab as some tris in the patch might be dark ->
you can turn off the shading of the surfaces on the right panel. 
Finally in you can use different Filters -> Cleanning and Repairing filters like T-vertices, erase zero are faces and so on, but at this mesh is non manifold you should not clean this with cleaning 
non manifold edges or vertexs

Then, you can extract useing Filters->Selection->Conditional Selection by Color of faces and using (r0 == 0) || (r1 == 0) || (r2 == 0) or something similar to get only the patch and save it as final_mesh.obj WITHOUT colors
for being used in s7_genTetMI_EHT.m (this final_mesh can be also the unclean one as long as it gives a inside point of the mesh with surfseeds, see s7_genTetMI_EHT). The final cleaned final_mipatch_surfmesh.obj
should be exported WITH colors as form here we get the patch nodes in s7_genTetMI_EHT.m

Finally we have the tetmesh.vtk :DDD
We apply different other scripts according to the application, for example we clean the scar, we clean the scar's fibers, we set the stimAHA nodes and so on.


See:

[10.22489/CinC.2023.275](https://doi.org/10.22489/CinC.2023.275)

[10.22489/CinC.2024.376](https://doi.org/10.22489/CinC.2024.376)