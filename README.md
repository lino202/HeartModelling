# HeartModelling

This repository contains scripts for defining **ventricular heart models**, including the **ventricular conduction system** and **engineered heart tissue (EHT)** + ventricular models.  

The code supports common input and output formats used in [3D Slicer](https://www.slicer.org/), [MeshLab](https://www.meshlab.net/), and [ParaView](https://www.paraview.org/) — open-source visualization tools typically used alongside these scripts to achieve advanced heart modeling workflows.


## 🚀 Features

- **Fiber Orientation** – Generation of myocardial fiber architecture using Laplacian-based or rule-based methods.  
- **Tetrahedralization** – Conversion of surface meshes into high-quality volumetric tetrahedral meshes for simulation.  
- **Ventricular Conduction System** – Creation of a physiologically realistic Purkinje and conduction network.  
- **Ventricular Spatial Heterogeneities** – Definition of regional heterogeneities based on Laplacian fields.  
- **Epicardial Patch Engraftment** – Integration of engineered heart tissue (EHT) patches with native ventricular geometry.  

## 🧩 Installation

1. **Install Python 3.X** and all required dependencies using `pip` or `conda`.  
   Some scripts are MATLAB-based, so MATLAB is also required to run those parts.

2. *(Optional)* It is recommended to use **Visual Studio Code** for Python development.

3. **Clone the repository:**
   ```sh
   git clone https://github.com/lino202/HeartModelling
   cd HeartModelling
   ```

4. *(Optional)* A Conda environment file (`environment[Linux/Win].yml`) is provided to recreate the an environment with all the dependencies:
   ```sh
   conda env create -f environment[Linux/Win].yml
   ```
   > 💡 **Note:** Linux is recommended, as [FEniCS](https://fenicsproject.org/) is used for computing fiber orientations, solving Laplacian equations, and performing mesh operations, among other tasks.

5. **Run example scripts:**  
   You can check the [`.vscode/launch.json`](.vscode/launch.json) file for examples of how to run scripts and what arguments they require.

---

## ⚙️ Usage

Documentation and code comments are currently limited, as this repository was originally developed for internal research purposes within the [BSICoS group](https://bsicos.i3a.es/es/). Every folder has a README file with a summary of the code contained in each folder. 
Usability improvements and better documentation are planned — and **community contributions are highly appreciated**!

In general:
- Python scripts accept command-line arguments. You can check the available options with:
  ```sh
  python /path-to-script/script.py --help
  ```
  Example scripts can be found under [`scripts/`](scripts/), specially, check [`scripts/make_model.sh`](scripts/make_model.sh)
- MATLAB scripts should be inspected directly in code to understand their parameters.

---

## 🤝 Contributing

Contributions make the open-source community such a great place to learn, inspire, and create.  
Any contributions — from bug fixes to documentation improvements — are **greatly appreciated**.

If you plan to contribute, please fork the repository, create a feature branch, and submit a pull request.

---

## 🙏 Acknowledgments

This code builds upon and integrates ideas from several open-source projects.  
The most important include:  
- [ldrb](https://github.com/finsberg/ldrb)  
- [fractal-tree](https://github.com/fsahli/fractal-tree)
