#Modify the files to be used in OpenCARP
import meshio
import argparse
import os
import numpy as np
import utils as ut
import time
import matplotlib.pyplot as plt
import seaborn as sns
# import nanomesh
from scipy.spatial import KDTree

def main():
    parser = argparse.ArgumentParser(description="Options")
    parser.add_argument('--file_path_fibers',        type=str, required=True)
    parser.add_argument('--unit',            type=str, required=True)
    parser.add_argument('--cellType',        type=str, default="tetra")
    parser.add_argument('--stimPointData',   type=str)
    parser.add_argument('--fibersPointData', type=str)
    parser.add_argument('--layersPointData', type=str)
    parser.add_argument('--outFolder',       type=str, required=True)
    parser.add_argument('--elemData',       type=str, required=False, help="Filed where the labels to be added to the elems are")
    parser.add_argument('--mesh_name',     type=str, required=True, help='name of the mesh of the endo surfaces to compute the FEC')
    parser.add_argument('--add_FEC', action='store_true', help='if especified, the FEC layer is added directly to the elements') #JRDZC 01/07/2026
    parser.add_argument('--domainType',    type=str, required=True, help='BiV (Biventricular) or LV')
    # parser.add_argument('--groundPointData', action='store_true', help='To choose a ground point for bidomain simulations')
    
    # parser.add_argument('--save' ,action='store_true',  help='save histogram tags')
    
    args = parser.parse_args()

    # --file_path_fibers         #Complete path to the mesh with the fibers and pacing sites
    # --unit              #Units of the mesh.  cm, mm or um
    # --cellType          #Cell type. Default value is tetra 
    # --stimPointData     #Name of the field with the Points where the stimuli will start. Right now only add 1 stimulus
    # --fibersPointData   #Point data for fiber orientation
    # --layersPointData   #Maxi removed it
    # --outFolder         #Path for results
    #--elemData           #Data in points to be included as element tags in the .elem file

    ht=os.path.split(args.file_path_fibers)
    

    #Open mesh
    mesh = meshio.read(args.file_path_fibers)
    if not os.path.isdir(args.outFolder): os.mkdir(args.outFolder)
    # fileName2Use = args.file_path_fibers.split(".")[0].split("/")[-1]
    fileName2Use=str(ht[1]).split(".")[0]
    # fileName2Use = ht[1](".")[0].split("/")[-1]
    
    #Switch to um as opencarp only seems to support that
    if args.unit=="cm":
        mesh.points = mesh.points * 10000
    elif args.unit=="mm":
        mesh.points = mesh.points * 1000
    elif args.unit=="um":
        pass
    else: raise ValueError("Only units in cm, mm or um are supported")

    #Save pts in carp format
    print("Getting points as .pts file-------------")
    ut.writePointsFile(mesh.points, os.path.join(args.outFolder, "{}.pts".format(fileName2Use)))

    fieldsPoints = list(mesh.point_data.keys())
    fieldsCells = list(mesh.cell_data.keys())
    
    #COnvert tags to CellData #JRDZC 18/03/2025
    if args.elemData: #Tags for elemData to be used in openCARP
        
        
        if args.elemData in fieldsCells:
            layersCells=mesh.cell_data[args.elemData]
            layersCells=layersCells[0]
            # np.array(layersCells)
            # layersCells=layersCells.astype(int)
            # a=2

        elif args.elemData in  fieldsPoints:
            layersPoints=mesh.point_data[args.elemData]
            layersCells=ut.points2Elements(mesh.cells_dict[args.cellType], layersPoints)
            # layersCells=layersPoints.copy()
            #Save the mesh with this tags
            mesh.cell_data[args.elemData]=layersCells

            #Save mesh with the modified units so if necessary, you can run this program again without multiplying the units
            # newNameMesh=os.path.join(ht[0],fileName2Use+"_{}.vtk".format(args.unit))

            if args.unit=="um":
                newNameMesh=os.path.join(ht[0],fileName2Use+".vtk")
            else: 
                newNameMesh=os.path.join(ht[0],fileName2Use+"_micrometers.vtk")
            # newNameMesh=os.path.join(ht[0],fileName2Use+"_micrometers.vtk")


            mesh.write(newNameMesh)

            unique_val, unique_counts = np.unique(layersCells, return_counts=True)
            Array_aux = np.concatenate((unique_val[:,None],unique_counts[:,None]),axis=1)
            content = str(Array_aux)
            meshName=ht[1].split(".")[0]
            with open(os.path.join(args.outFolder,meshName+"_labels.txt"), "w") as file:
                
                file.write(content)
                file.close()
            # f = open(, "x")

            #Histogram of elements 
            if unique_val.shape[0]<12: #If there are less labels
                for aux_tag in np.arange(0,unique_val.shape[0]-1,dtype=int):
                    print(unique_val[aux_tag], unique_counts[aux_tag])
            # print("The lower borderZoneThresBottom is {}".format(borderZoneThresBottom))
            # f, axis_hist = plt.subplots(figsize=(.15, .85))
            # axis_hist.set_title('Histograms of elem tags') #JRDZC Add 14/01/2025
            # sns.histplot(x=layersCells, ax=axis_hist, binwidth=1)
            # axis_hist.set_ylabel("Count", fontdict=dict(weight='bold'))
            # axis_hist.set_xlabel("Element tags", fontdict=dict(weight='bold'))
            # sns.despine(ax=axis_hist)
            # fileName2Use=ht[1].split(".")
            # fileName2Use="elemTagsHist"+ fileName2Use +".png"
            # #Save plot
            # plt.savefig(os.path.join(args.outFolder, "elemTagsHist.png"), dpi=400) if args.save else plt.show(block=True)
    else:
        layersCells=np.zeros(mesh.cells_dict[args.cellType].shape[0], dtype=np.int_)
        
        
    # Add FEC directly to elements
    if args.add_FEC:
            FEC_flag=2
            #FEC layer will be all the points of 2 element depth from endo
            #Read the mesh surfaces
            LVEndoName = args.mesh_name + "_lv_endo.vtu"
            endoLVMesh = meshio.read(os.path.join(ht[0], "mesh", LVEndoName))# JRDZC

            if args.domainType.lower() == "biv":
                RVEndoName = args.mesh_name + "_rv_endo.vtu"
                endoRVMesh = meshio.read(os.path.join(ht[0], 'mesh', RVEndoName))# JRDZC
            
            
            #Transform units as mesh
            if args.unit=="cm":
                endoLVMesh.points = endoLVMesh.points * 10000
                if args.domainType.lower() == "biv":
                    endoRVMesh.points = endoRVMesh.points * 10000
            elif args.unit=="mm":
                endoLVMesh.points = endoLVMesh.points * 1000
                if args.domainType.lower() == "biv":
                    endoRVMesh.points = endoRVMesh.points * 1000
            elif args.unit=="um":
                pass
            else: raise ValueError("Only units in cm, mm or um are supported")

            endoLVPoints = endoLVMesh.points
            

            if args.domainType.lower() == "biv":
                endoRVPoints = endoRVMesh.points
            else:
                endoRVPoints = np.array([])
    
            #Find points within the surfaces mesh- Jimena 22/07/2026
            treeMesh = KDTree(mesh.points)
            _ , idxsLV = treeMesh.query(endoLVPoints, k=1)

            # _ , idxsRV = treeMesh.query(endoRVPoints, k=1)
    
            # all_markers = np.zeros((mesh.points.shape[0]))
            # all_markers[idxsRV] = FEC_flag
            # all_markers[idxsLV] = FEC_flag
            # idxs = [*idxsRV, *idxsLV]


            if args.domainType.lower() == "biv":
                _ , idxsRV = treeMesh.query(endoRVPoints, k=1)
                # all_markers[idxsRV] = FEC_flag
                idxs = [*idxsRV, *idxsLV]
    
            else:
                idxs = [*idxsLV]



            elementsSurface=mesh.cells_dict['tetra']
            elemS=np.isin(elementsSurface, idxs) #FInd elements with those points in the surface
            cell2Choose=np.sum(elemS,axis=1) #Sum , to find all elemets with at least1 point in the surface
            cell2Choose=cell2Choose!=0

            layersCellsFEC= layersCells.copy()
            selected = layersCellsFEC[cell2Choose]
            # Modify and assign back directly
            layersCellsFEC[cell2Choose] = 200 + (selected % 100)


            unique_val, unique_counts = np.unique(layersCellsFEC, return_counts=True)
            Array_aux = np.concatenate((unique_val[:,None],unique_counts[:,None]),axis=1)
            content = str(Array_aux)
            meshName=ht[1].split(".")[0]
            with open(os.path.join(args.outFolder,meshName+"_labelswithFEC_last.txt"), "w") as file:
                
                file.write(content)
                file.close()

            mesh.cell_data[args.elemData+"_FEClast"]=layersCellsFEC

            if args.elemData: #Save new cell field
                mesh.write(newNameMesh)

            #Save cells in carp format
            print("Getting cells as with FEC .elem file-------------")
            # ut.writeCellsFile(mesh.cells_dict[args.cellType], os.path.join(args.outFolder, "{}.elem".format(fileName2Use)), cellType=ut.meshioOCCellsMap[args.cellType],layers)
            ut.writeCellsFile(mesh.cells_dict[args.cellType], os.path.join(args.outFolder, "{}.elem".format(fileName2Use)),layersCellsFEC, cellType=ut.meshioOCCellsMap[args.cellType])#Add the tags to cells. #JRDZC 20/03/2025
            #writeCellsFile(arr, outName, cellType="Tt", tags)

    else: #If fec is not added
        #Save cells in carp format
            print("Getting cells without FEC as .elem file-------------")
            # ut.writeCellsFile(mesh.cells_dict[args.cellType], os.path.join(args.outFolder, "{}.elem".format(fileName2Use)), cellType=ut.meshioOCCellsMap[args.cellType],layers)
            ut.writeCellsFile(mesh.cells_dict[args.cellType], os.path.join(args.outFolder, "{}.elem".format(fileName2Use)),layersCells, cellType=ut.meshioOCCellsMap[args.cellType])#Add the tags to cells. #JRDZC 20/03/2025
            #writeCellsFile(arr, outName, cellType="Tt", tags)



    #Create .vtx files of point data of interest
    if args.stimPointData:
        fields = list(mesh.point_data.keys())
        for fd in fields:
            if "stim" in fd: #Search for word stim and asume they are stimulus points
                print("Getting stim nodes as vtx file -------------")
                tmp = mesh.point_data[fd]
                tmp = (tmp==1).nonzero()[0]
                #Save
                # ut.writeStimVtxFile(tmp, os.path.join(args.outFolder, "{}.vtx".format(fd)))
                ut.writeStimVtxFile(tmp, os.path.join(args.outFolder, "{}_{}.vtx".format(fd,fileName2Use)),"extra")

                


    #Add fibers to cell data
    # if fibers are already or you want just default fibers from meshtool just dont pass the argument
    if args.fibersPointData:
        
        if args.fibersPointData in fieldsCells:
            fibsCells=mesh.cell_data[args.fibersPointData]
            fibsCells=fibsCells[0]
            # aux=2

        elif args.fibersPointData in  fieldsPoints:

            print("Getting fibers for elem as .lon file-------------")
            fibsCells = np.mean(mesh.point_data[args.fibersPointData][mesh.cells_dict["tetra"]], axis=1)
            fibsCells = ut.getArrNormalization(fibsCells)

        #Save
        ut.writeFibsFile(fibsCells, os.path.join(args.outFolder, "{}.lon".format(fileName2Use)))

    print("Finished:",args.file_path_fibers)

    #Add tag to cell data for meshtool to understand
    # if hasattr(args, "layersPointData"):
        # print("Getting cells tags in the vtk file -------------")
        # fibsCells = np.mean(mesh.point_data["fibers"][mesh.cells_dict["tetra"]], axis=1)
        # fibsCells = getArrNormalization(fibsCells)
        # mesh.cell_data["fibers"] = [fibsCells]
        # writeFlag = 1

    # We are not using meshtool as meshio saves fibs in FIELD data and meshtool wants them in VECTOR (need more research)
    # #Convert mesh to carp format
    # print("Converting mesh to CARP format")
    # cmdMesh = 'meshtool convert -imsh={0} -omsh={1}/{2}'.format(args.file_path_fibers, args.outFolder, args.file_path_fibers.split(".")[0].split("/")[-1])
    # outMesh = os.system(cmdMesh)
    # if outMesh==0: print("Mesh conversion successfully") 
    # else: print("Mesh conversion failure")

    # #Find the ground point to be used in the bidomain simulations
    # if args.groundPointData:
    #     #Aha segments 12(layers, AHASegs=12), epicardio (layers, xv=1), no scar, ni BZ, (mesh, layers_scar=)
    #     aha_mesh=meshio.read(os.path.join(ht[0],'layers','laplacians.vtk'))
        
    #     fields = list(mesh.point_data.keys())
    #     for fd in fields:
    #         if "stim_AHA" in fd:
    #             print("Getting stim nodes as vtx file -------------")
    #             tmp = mesh.point_data[fd]
    #             tmp = (tmp==1).nonzero()[0]
    #             # ut.writeStimVtxFile(tmp, os.path.join(args.outFolder, "{}.vtx".format(fd)))
    #             ut.writeStimVtxFile(tmp, os.path.join(args.outFolder, "{}_{}.vtx".format(fd,fileName2Use)))


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time was {} s".format(time.time() - start))