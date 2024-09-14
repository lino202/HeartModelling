import os  
import argparse
import numpy as np
import meshio

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--dataPath',type=str, required=True, help='path to data')
parser.add_argument('--outName',type=str, required=True)
parser.add_argument('--vtkMesh',type=str, required=True, help="vtk mesh with or without previous node classification, if 'layers_mi' it comes from scar determination MI and if not 'layers_mi' comes form healthy")
parser.add_argument('--infAsHealthy', action='store_true', help='if especified, MI is not taken into account')
args = parser.parse_args()


transmural_pathC = os.path.join(args.dataPath, 'layers', "transmural_distLV.vtu") 
inputVtk = os.path.join(args.dataPath, 'mesh', '{}.vtk'.format(args.vtkMesh))


validKeys = ["endo", "mid", "epi", "myo", "scar", "uncertain", "bz"]
myo_flag = 1
scar_flag = 8
endo_flag = 3
mid_flag = 4
epi_flag = 5
uncertain_flag = 6
bz_flag = 7

endo_per = 40; endo_per = endo_per /100
epi_per = 25; epi_per = epi_per /100

phi0 = -1
phi1 = 1

#Read Data
trans_distC = meshio.read(transmural_pathC)
meshVtk = meshio.read(inputVtk)
#Change data reference points for incorporating endo mid and epi
if "layers_mi" in meshVtk.point_data.keys():
    all_points = meshVtk.point_data["layers_mi"]
else:
    all_points = np.zeros((meshVtk.points.shape[0]))
    
all_points[all_points==2] = uncertain_flag
all_points[all_points==3] = bz_flag
all_points[all_points==4] = scar_flag

#Calculate layers
phi_endo = (1-endo_per) * phi0 + endo_per * phi1    #thresholds
phi_epi = epi_per * phi0 + (1-epi_per) * phi1




transC_endo = np.zeros((meshVtk.points.shape[0])) 
transC_endo[trans_distC.point_data['f_20']<phi_endo] = 1
transC_endo = transC_endo.astype(bool)

transC_epi = np.zeros((meshVtk.points.shape[0]))
transC_epi[trans_distC.point_data['f_20']>phi_epi] = 1
transC_epi = transC_epi.astype(bool)

transC_mid = np.zeros((meshVtk.points.shape[0])) 
transC_mid[(trans_distC.point_data['f_20']<=phi_epi) & (trans_distC.point_data['f_20']>=phi_endo)] = 1
transC_mid = transC_mid.astype(bool)

algo_points = np.zeros((meshVtk.points.shape[0])) 

#We saw that algo 2 is more biomimetic
#Algo 2 use A, B and C
algo_points[transC_epi] = epi_flag
algo_points[transC_mid] = mid_flag
algo_points[transC_endo] = endo_flag

if not args.infAsHealthy:
    endoBZ_points = np.zeros((meshVtk.points.shape[0])) 
    endoBZ_points[np.where((all_points==bz_flag) & (algo_points==endo_flag))] = 1
    midBZ_points = np.zeros((meshVtk.points.shape[0])) 
    midBZ_points[np.where((all_points==bz_flag) & (algo_points==mid_flag))] = 1
    epiBZ_points = np.zeros((meshVtk.points.shape[0])) 
    epiBZ_points[np.where((all_points==bz_flag) & (algo_points==epi_flag))] = 1
    algo_points[all_points==bz_flag] = bz_flag
    algo_points[all_points==scar_flag] = scar_flag

point_data = meshVtk.point_data
nsets = {}
for tissueType in validKeys:
    point_data[tissueType] = np.zeros((meshVtk.points.shape[0]))
    point_data[tissueType][algo_points==globals()["{}_flag".format(tissueType)]] = 1
    nsets["{}_nodes".format(tissueType)] = np.where(point_data[tissueType] == 1)[0]
point_data["layers_tissues"] = algo_points


if not args.infAsHealthy:
    point_data["endoBZ"] = endoBZ_points
    point_data["midBZ"] = midBZ_points
    point_data["epiBZ"] = epiBZ_points
    nsets["endobz_nodes"] = np.where(endoBZ_points==1)[0]
    nsets["midbz_nodes"] = np.where(midBZ_points==1)[0]
    nsets["epibz_nodes"] = np.where(epiBZ_points==1)[0]

#SaveData
meshOutVtk = meshio.Mesh(meshVtk.points, meshVtk.cells, point_data=point_data)
meshOutVtk.write(os.path.join(args.dataPath, "{}.vtk".format(args.outName)))

# meshOutInp = meshio.Mesh(meshVtk.points, meshVtk.cells, point_sets=nsets)
# meshOutInp.write(os.path.join(args.dataPath, "{}.inp".format(args.outName)))
