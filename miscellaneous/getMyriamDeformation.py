import os 
import numpy as np
import argparse
import meshio
from utils import writeFibers4JSON
from scipy.interpolate import RBFInterpolator

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshInvivo',type=str, required=True, help='path to data')
parser.add_argument('--meshExvivo',type=str, required=True, help='path to data')
# parser.add_argument('--surfFibers',type=str, required=True, help='path to data')
args = parser.parse_args()

meshInvivo = meshio.read(args.meshInvivo)
meshExvivo = meshio.read(args.meshExvivo)
# surfFibers = meshio.read(args.surfFibers)

lmsDiff = {}
for key in meshInvivo.point_data.keys():
    if key != "all":
        B = meshInvivo.points[np.where(meshInvivo.point_data[key]==1)[0][0],:]
        A = meshExvivo.points[np.where(meshExvivo.point_data[key]==1)[0][0],:]
        lmsDiff[key] = B - A


name = args.meshExvivo.split("/")[-1].split(".")[0]
path = args.meshExvivo.split(name)[0]

with open(os.path.join(path, "lmsDiffs.txt"), "w") as file:
    file.write("#Name x,y,z diff\n")
    for key in lmsDiff.keys():
        file.write("{0:s},{1:f},{2:f},{3:f}\n".format(key,lmsDiff[key][0],lmsDiff[key][1], lmsDiff[key][2] ))

# fibers2 = RBFInterpolator(surfFibers.points, surfFibers.point_data["dti_fibers"], neighbors=100)(meshExvivo.points)
# fibersNorm = np.linalg.norm(fibers2, axis=1)
# fibers2 = fibers2 / np.array([fibersNorm, fibersNorm, fibersNorm]).T

# writeFibers4JSON(os.path.join(path, "exVivoSurfFibers.txt"), fibers2)

# meshOut = meshio.Mesh(meshExvivo.points, meshExvivo.cells, point_data={"dti_fibers": fibers2})
# meshOut.write(os.path.join(path, "{}_lms_fibers.vtk".format(name)))
