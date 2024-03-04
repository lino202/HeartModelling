import os
import random
import meshio
import numpy as np 
import argparse
from lib.utils import checkEndBranchesOrder, getBranches, getOutliersTh, getProjectionDir, getProjectionMag, getLinearPath, getEdges, reorderPurkMesh, saveVtkInpMesh1D
from lib.utils import checkRepeatedPoints, smoothProjection, updatePointsEdgesBranches

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--data_path',type=str, required=True, help='path to data')
parser.add_argument('--out_name',type=str, required=True, help='output file name')
parser.add_argument('--endo_per',type=int, required=True, help='endo percentage')
parser.add_argument('--epi_per',type=int, required=True, help='epi percentage')
parser.add_argument('--subendo_window',type=int, required=True, help='subendo goes from mid-endo threshold to this percentage of endo')
parser.add_argument('--intramyo_window',type=int, required=True, help='intramyo window is the middle width transmural wall in which purk endnodes are going to be projected')
parser.add_argument('--meanMag',type=int, required=True, help='number of nodes to average for magnitud of the projection')
parser.add_argument('--meanNor',type=int, required=True, help='number of nodes to average for normal direction of the projection')
parser.add_argument('--project_intramyo', action='store_true', help='if specified, project subEndo enpoints to intramyo')
parser.add_argument('--debug_vtk', action='store_true', help='if especified, save all branches to vtk and inp')
parser.add_argument('--proj_linear', action='store_true', help='if especified, linear projection into intramid otherwise folows the already curved branch')
parser.add_argument('--intramyo_percentage',type=int, help='percentage of endpoints to project to intramyo')
parser.add_argument('--projectRV', action='store_true', help='if especified, projects RV')
parser.add_argument('--domainType',type=str, required=True, help='BiV (Biventricular) or LV')
args = parser.parse_args()

#Inputs
lvSurfMesh = meshio.read(os.path.join(args.data_path, "mesh", "lv_endo.obj"))  #normals corrected
if args.domainType == "BiV": rvSurfMesh = meshio.read(os.path.join(args.data_path, "mesh", "rv_endo.obj"))
csBundle = meshio.read(os.path.join(args.data_path, "stim", "stim_cs", "mainCSBundle.vtk"))
if args.domainType == "BiV": transDistRV = meshio.read(os.path.join(args.data_path, "layers", "transmural_distRV.vtu"))
transDistLV = meshio.read(os.path.join(args.data_path, "layers", "transmural_distLV.vtu"))
outPath = os.path.join(args.data_path, "stim", "stim_cs")
outName = args.out_name

#Perrotti definitions, must be consistent with the ones used
endoPer = args.endo_per / 100
epiPer = args.epi_per / 100
subendoWindow = args.subendo_window / 100
intramyoWindow = args.intramyo_window
phi0 = -1
phi1 = 1
phiEndo = (1-endoPer) * phi0 + endoPer * phi1    # thresholds
phiEpi = epiPer * phi0 + (1-epiPer) * phi1
subendoWindow = [phi0 - ((phi0 - phiEndo) * subendoWindow)  , phiEpi]
intramyoWindow = [phiEndo , phiEpi] 
# intramyoWindow = [phiEndo + (abs(phiEndo - phiEpi) / intramyoWindow)  , phiEndo + 2*(abs(phiEndo - phiEpi) / intramyoWindow)]

#MAIN BUNDLE------------------------------------------------------------------------
# 1 Reconstruc HisBundle from AV node to bifurcation
nsetsSimple={}
avNodeIdx = np.where(csBundle.point_data["av_node"]==1)[0][0]
hisBifNodeIdx = np.where(csBundle.point_data["his_bifur_node"]==1)[0][0]
points, edges =  getLinearPath(csBundle.points[avNodeIdx,:], csBundle.points[hisBifNodeIdx,:])
nsetsSimple["av_node"] = [avNodeIdx]     # nsets must be iterable
nsetsSimple["av_his"] = [nodeIdx for nodeIdx in range(points.shape[0])]
nsetsSimple["his_bifur_node"] = [hisBifNodeIdx]


# First project the geodesic bundles into subendo
print("---------Projecting Main Bundles-----------")
if args.domainType == "BiV":
    branches2Project = ["rvb", "lva", "lvp", "his_rv_geo", "his_lv_geo"]
elif args.domainType == "LV":
    branches2Project = ["lva", "lvp", "his_lv_geo"]
else: raise ValueError("domainType must be BiV or LV") 

for key in branches2Project:
    print("Processing {}".format(key))
    branchIdxs = csBundle.point_data[key]
    csBundleNodes = csBundle.points
    branchIdxs = np.where(branchIdxs==1)[0]

    #Calculate projection dir and magnitude for projection points and new edges
    dirs = getProjectionDir(csBundleNodes[branchIdxs,:], lvSurfMesh if "lv" in key else rvSurfMesh, k=args.meanNor)
    mags = getProjectionMag(csBundleNodes[branchIdxs,:], transDistLV if "lv" in key else transDistRV, subendoWindow, k=args.meanMag)
    mags = np.expand_dims(mags, axis=1)
    mags = np.repeat(mags, repeats=3, axis=1)
    tmpPoints = csBundleNodes[branchIdxs,:] + dirs * mags
    tmpEdges = getEdges(tmpPoints)

    #add points, edges and nsets
    tmpEdges = tmpEdges + points.shape[0]
    nsetsSimple[key] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + tmpPoints.shape[0])]
    if key == "lva": LVAfirstIdx = np.min(tmpEdges); LVAlastIdx = np.max(tmpEdges)
    elif key == "lvp": LVPfirstIdx = np.min(tmpEdges); LVPlastIdx = np.max(tmpEdges)
    elif key == "rvb": RVBfirstIdx = np.min(tmpEdges); RVBlastIdx = np.max(tmpEdges)
    elif key == "his_rv_geo":
        hisRVGeoInitIdx = np.min(tmpEdges)
        tmpEdges = np.concatenate((tmpEdges, np.array([[RVBfirstIdx, np.max(tmpEdges)]])), axis=0)
    elif key == "his_lv_geo":
        hisLVGeoInitIdx = np.min(tmpEdges)
        maxEdge = np.max(tmpEdges)
        tmpEdges = np.concatenate((tmpEdges, np.array([[LVAfirstIdx, maxEdge]])), axis=0)
        tmpEdges = np.concatenate((tmpEdges, np.array([[LVPfirstIdx, maxEdge]])), axis=0)
    else: raise ValueError("Branch not implemented") 


    edges = np.concatenate((edges, tmpEdges), axis=0)
    points = np.concatenate((points, tmpPoints), axis=0)
    if key in branches2Project[:3]:
        nsetsSimple["{}_end".format(key)] = [points.shape[0]-1]


# Second, recalculate linear his bundle branches
if args.domainType == "BiV":
    tmpPoints, _ =  getLinearPath(points[hisBifNodeIdx,:], points[hisRVGeoInitIdx,:])
    tmpPoints = tmpPoints[1:-1]        # both points are already in the mesh
    tmpEdges = getEdges(tmpPoints)
    tmpEdges = tmpEdges + points.shape[0]
    nsetsSimple["his_rv_linear"] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + tmpPoints.shape[0])]
    minEdge = np.min(tmpEdges); maxEdge = np.max(tmpEdges)
    tmpEdges = np.concatenate((tmpEdges, np.array([[hisRVGeoInitIdx, maxEdge]])), axis=0)
    tmpEdges = np.concatenate((tmpEdges, np.array([[hisBifNodeIdx, minEdge]])), axis=0)
    edges = np.concatenate((edges, tmpEdges), axis=0)
    points = np.concatenate((points, tmpPoints), axis=0)

tmpPoints, _ =  getLinearPath(points[hisBifNodeIdx,:], points[hisLVGeoInitIdx,:])
tmpPoints = tmpPoints[1:-1]        # both points are already in the mesh
tmpEdges = getEdges(tmpPoints)
tmpEdges = tmpEdges + points.shape[0]
nsetsSimple["his_lv_linear"] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + tmpPoints.shape[0])]
minEdge = np.min(tmpEdges); maxEdge = np.max(tmpEdges)
tmpEdges = np.concatenate((tmpEdges, np.array([[hisLVGeoInitIdx, maxEdge]])), axis=0)
tmpEdges = np.concatenate((tmpEdges, np.array([[hisBifNodeIdx, minEdge]])), axis=0)
edges = np.concatenate((edges, tmpEdges), axis=0)
points = np.concatenate((points, tmpPoints), axis=0)

checkRepeatedPoints(points)

# Make the projection for every Purkinje tree and unify all
print("----------Making Purkinje Tree Projection----------")
if args.domainType == "BiV":
    branches2Project = ["lva", "lvp", "rvb"]
elif args.domainType == "LV":
    branches2Project = ["lva", "lvp"]
else: raise ValueError("domainType must be BiV or LV") 

purkBranches = {}
purkSimple = {}
tmpPurkBranches = {}
for key in branches2Project:
    #Load mesh points and edges
    print("Processing {}".format(key))
    meshPurk = meshio.read(os.path.join(args.data_path, "stim", "stim_cs", "finalBundles", "{}.vtu".format(key)))
    tmpPoints = meshPurk.points
    tmpEdges = meshPurk.cells_dict["line"]

    #Reorder mesh for having continuos indexing per branch
    tmpPoints, tmpEdges = reorderPurkMesh(tmpPoints, tmpEdges)

    #Calculate projection dir and magnitude for projection points
    if args.projectRV or key!="rvb":
        dirs = getProjectionDir(tmpPoints, lvSurfMesh if "lv" in key else rvSurfMesh, k=args.meanNor)
        mags = getProjectionMag(tmpPoints, transDistLV if "lv" in key else transDistRV, subendoWindow, k=args.meanMag)
        mags = np.expand_dims(mags, axis=1)
        mags = np.repeat(mags, repeats=3, axis=1)
        tmpPoints = tmpPoints + dirs * mags    
        tmpPoints = smoothProjection(tmpPoints, tmpEdges)

    #Add points, edges and nsets
    tmpEdges = tmpEdges + points.shape[0] - 1
    idxs = np.where(tmpEdges == (points.shape[0] - 1))
    if key == "lva": endpointRefIdx = LVAlastIdx
    elif key == "lvp": endpointRefIdx = LVPlastIdx
    elif key == "rvb": endpointRefIdx = RVBlastIdx
    else: raise ValueError("Branch not implemented") 
    
    tmpEdges[idxs] = endpointRefIdx
    purkBranches["{}_branches".format(key)] = getBranches(tmpEdges, endpointRefIdx, key)
    
    #define nsets (inp) and pointData (vtk)
    purkSimple[key + "_purk"] = [nodeIdx for nodeIdx in range(points.shape[0] , points.shape[0] + tmpPoints.shape[0]-1)]
    endnodesPurk, count = np.unique(tmpEdges.flatten(), return_counts=True)
    purkSimple[key + "_purk_endnodes"] = endnodesPurk[count==1]
    try:
        purkSimple["purk_endnodes"] = np.concatenate((purkSimple["purk_endnodes"],endnodesPurk[count==1]))
    except KeyError:
        purkSimple["purk_endnodes"] = endnodesPurk[count==1]

    tmpPurkBranches = {**tmpPurkBranches, **purkBranches["{}_branches".format(key)]}
    edges = np.concatenate((edges, tmpEdges), axis=0)
    points = np.concatenate((points, tmpPoints[1:]), axis=0)


if args.debug_vtk: 
    nsets = {**nsetsSimple, **purkSimple, **tmpPurkBranches}
else:
    nsets = {**nsetsSimple, **purkSimple}

checkRepeatedPoints(points)

# Now we can propagate linearly the end branches following . Garcia-Bustos et al, 
# “Changes in the spatial distribution of the Purkinje network after acute myocardial infarction in the pig”


# ------------------------- HEALTHY --------------------------------------------------------------------------
if args.project_intramyo: 
    print("-----------Making projection into mid-myocardium of End Branches------------")
    tmpPurkBranches = {}  
    del purkSimple["purk_endnodes"]
    
    if not args.projectRV and args.domainType == "BiV": 
        del purkBranches["rvb_branches"]
        del purkSimple["rvb_purk_endnodes"]

    for key in purkBranches.keys():
        print("Proccessing {}".format(key))
        branchType = key.split("_")[0]
        del purkSimple["{}_purk_endnodes".format(branchType)]
        idxs = checkEndBranchesOrder(purkBranches[key], branchType)
        idxs2Mid = random.sample(idxs, int(len(idxs)*(args.intramyo_percentage/100)))

        for i in idxs2Mid:
            branchName = "{}_endBranch_{}".format(branchType,i)
            branchPoints = sorted(purkBranches[key][branchName])
            endNodePoint = np.expand_dims(points[max(branchPoints),:], axis=0)
            dirs = getProjectionDir(endNodePoint, lvSurfMesh if "lv" in key else rvSurfMesh, k=args.meanNor)
            mags = getProjectionMag(endNodePoint, transDistLV if "lv" in key else transDistRV, intramyoWindow, k=args.meanMag)
            
            #Reference de joint, create projection and update Points and Edges
            jointNodeIdx = min(branchPoints)
            #Linear
            if args.proj_linear:
                newBranchPoints, newBranchEdges = getLinearPath(points[jointNodeIdx,:], np.squeeze(endNodePoint + dirs * mags), step=0.6)
            else:
                mags = np.linspace(0,mags, len(branchPoints))
                mags = np.repeat(mags, repeats=3, axis=1)
                newBranchPoints = points[branchPoints,:] + dirs * mags
                newBranchEdges = getEdges(newBranchPoints)

            branchPoints.remove(jointNodeIdx)
            points, edges, purkSimple, purkBranches = updatePointsEdgesBranches(points, edges, purkSimple, purkBranches, branchPoints)
            
            #Add new edges and points
            newBranchEdges = newBranchEdges + points.shape[0] - 1
            newBranchEdges[np.where(newBranchEdges == points.shape[0] - 1)] = jointNodeIdx
            
            newBranchIndex = sorted(list(np.unique(newBranchEdges.flatten())))
            del purkBranches[key][branchName]
            purkBranches[key][branchName+ "_intramyo"] = newBranchIndex
            purkSimple["{}_purk".format(branchType)] = np.concatenate((purkSimple["{}_purk".format(branchType)] , newBranchIndex[1:]))

            edges = np.concatenate((edges, newBranchEdges), axis=0)
            points = np.concatenate((points, newBranchPoints[1:]), axis=0)
            
    uniqueEdges, count = np.unique(edges, return_counts=True)   
    uniqueEdges = uniqueEdges[count==1]
    #TODO calculate branch specific endpoints using the dict branches and the enpoints values
    purkSimple["purk_endnodes"] = uniqueEdges[uniqueEdges!=nsetsSimple["av_node"]] 

    # nsets= nsetsSimple
    if args.debug_vtk: 
        for key in purkBranches.keys():
            tmpPurkBranches = {**tmpPurkBranches, **purkBranches[key]}
        nsets = {**nsetsSimple, **purkSimple, **tmpPurkBranches}
    else:
        nsets = {**nsetsSimple, **purkSimple}



# Save
print("-----------Saving------------")
saveVtkInpMesh1D(points, edges, nsets, outPath, outName)
