import os 
import numpy as np
import argparse
import meshio

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--file1',type=str, required=True, help='path to data')
parser.add_argument('--file2',type=str, required=True, help='path to data')

args = parser.parse_args()

mesh1 = meshio.read(args.file1)
mesh2 = meshio.read(args.file2)
versors1 = mesh1.point_data["dti-fibers"]
versors2 = mesh2.point_data["dti-fibers"]

# versors1 = np.array([])
# versors2 = np.array([])

# with open(file1) as file:
#     while True:
#         line = file.readline()
#         if line == "": break
#         elif line[0] == "#": pass
#         else:
#             row = line.split("\n")[0].split(",")
#             row = np.array(row).astype(np.float)
#             versors1 = np.concatenate((versors1, np.expand_dims(row, axis=0))) if versors1.size else np.expand_dims(row, axis=0)

# with open(file2) as file:
#     while True:
#         line = file.readline()
#         if line == "": break
#         elif line[0] == "#": pass
#         else:
#             row = line.split("\n")[0].split("[")[1].split("]")[0].split(",")
#             row = np.array(row).astype(np.float)
#             versors2 = np.concatenate((versors2, np.expand_dims(row, axis=0))) if versors2.size else np.expand_dims(row, axis=0)

if versors2.shape != versors1.shape:
    raise ValueError("Different shapes!! Wrong files?")


similarity = []

for i in range(versors2.shape[0]):
    similarity.append(np.dot(versors1[i,:], versors2[i,:]))

print(np.mean(np.abs(similarity)))