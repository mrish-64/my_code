#"Framework for Wrapping Binary Swarm Optimizers to the Hybrid Parallel Cooperative Coevolving Version"
In this project, the source code of the swarm* is presented. We recommend first using and setting up this swarm* project before the serial swarm project (due to its importance).
# Used Environment
## Python Version
python 3.10.6 64 bit
## Local Packages Installed
matplotlib==3.5.3
numpy==1.23.2
> Use `pip install` to install the packages
## IDE info
Visual Studio Code
* Version: 1.70.2 (user setup)

* Commit: e4503b30fc78200f846c62cf8091b76ff5547662

* Date: 2022-08-16T05:35:13.448Z

* OS: Windows_NT x64 10.0.14393
#HowTo use
1. Copy the whole directory structure to your "D:\My_Code"
2. Only set the value of hardcoded parameters in optimize.py (optional) and run the `D:\My_Code\optimize.py` file.
3. Each embedded swarm algorithm parameters are in its directory and relevant .py file (i.e. D:\my_code\_HHO\HHO.py)
4. The swarm* parameters are in the optimize.py file .
5. To select the benchmark function use `D:\my_code\functions.py` and there set the default argument.
6. We said sub-search-space, "don't care (dc)" in this source code.
7. You can change the stride parameter from line 199. 
8. Number of processes is set to number of your CPU cores.
9. You can change the dimension and solution length from line 14.(In the paper we use dimension=10 and length=310) 
## Selecting the swarm algorithm to use
In lines 160-166 uncomment the preferred swarm algorithm line and comment on all the other swarm name lines.