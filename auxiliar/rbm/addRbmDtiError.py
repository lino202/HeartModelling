'''Add the discrepancy or error between RBM or DWI obtained fibers'''

import os
import numpy as np
import argparse
import meshio
import pandas as pd

params = ["Theta mean", "Theta std", "Theta median", "Theta min", "Theta max"]

parser = argparse.ArgumentParser(description="Options")
parser.add_argument('--meshPath',type=str, required=True, help='path to data, with dwi and rbm fibers')
parser.add_argument('--resExcel',type=str, required=True, help='path to results excel')
args = parser.parse_args()

mesh = meshio.read(args.meshPath)

for key in mesh.point_data.keys():
    if 'dti' in key: dtiName = key
    if 'rbm' in key: rbmName = key
dtiFibers  = mesh.point_data[dtiName]
rbmVersors = mesh.point_data[rbmName]

dotProduct = np.sum(np.multiply(dtiFibers, rbmVersors), axis=1)
normProduct = np.multiply(np.linalg.norm(dtiFibers, axis=1), np.linalg.norm(rbmVersors, axis=1))
thetas = np.rad2deg(np.arccos(np.abs(dotProduct / normProduct)))


mesh.point_data["thetas"] = thetas 
mesh.write(os.path.join(args.meshPath))

res = {}
res["Theta mean"]   = np.nanmean(thetas)
res["Theta std"]    = np.nanstd(thetas)
res["Theta median"] = np.nanmedian(thetas)
res["Theta min"]    = np.nanmin(thetas)
res["Theta max"]    = np.nanmax(thetas)

indexs = ["_".join(args.meshPath.split("/")[-3:])]
stats  = np.ones(len(params)) * np.nan
for i, param in enumerate(params):
    try:
        stats[i] = res[params[i]]
    except KeyError:
        pass
df = pd.DataFrame([stats], index=indexs, columns=params)
if not os.path.exists(args.resExcel):
    df.to_excel(args.resExcel, sheet_name='sheet1')
else:
    with pd.ExcelWriter(args.resExcel, engine="openpyxl", mode='a',if_sheet_exists="overlay") as writer:
        startrow = writer.sheets['sheet1'].max_row
        df.to_excel(writer, sheet_name='sheet1', startrow=startrow, header=False)