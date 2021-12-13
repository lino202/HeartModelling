import os 
import numpy as np



sample  = "sampleMA_Control2"
rbmFile = "./fibers/{}/long_fibers.txt".format(sample)
expFile = "./Data_Electra_DWI/{}/electraSlicer_tetfibers.txt".format(sample)



rbmVersors = np.array([])
expVersors = np.array([])

with open(rbmFile) as file:
    while True:
        line = file.readline()
        if line == "": break
        elif line[0] == "#": pass
        else:
            row = line.split("\n")[0].split(",")
            row = np.array(row).astype(np.float)
            rbmVersors = np.concatenate((rbmVersors, np.expand_dims(row, axis=0))) if rbmVersors.size else np.expand_dims(row, axis=0)

with open(expFile) as file:
    while True:
        line = file.readline()
        if line == "": break
        elif line[0] == "#": pass
        else:
            row = line.split("\n")[0].split("[")[1].split("]")[0].split(",")
            row = np.array(row).astype(np.float)
            expVersors = np.concatenate((expVersors, np.expand_dims(row, axis=0))) if expVersors.size else np.expand_dims(row, axis=0)

if expVersors.shape != rbmVersors.shape:
    raise ValueError("Different shapes!! Wrong files?")


similarity = []

for i in range(expVersors.shape[0]):
    similarity.append(np.dot(rbmVersors[i,:], expVersors[i,:]))

print(np.mean(np.abs(similarity)))