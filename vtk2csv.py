import subprocess
import os

pvpython_path = "C:\\Program Files\\ParaView 5.11.2\\bin\\pvpython.exe"

run_folder = '11.45.16_45kW_CF4_port1_16stream'
main_dir = os.path.join(os.getenv('USERPROFILE'), 'Desktop', 'PFAS_Modeling', 'cfs_runs')
destruct_file = os.path.join(main_dir, run_folder, 'excel\\destruct.csv')
destruct_file = destruct_file.replace('\\','/')
script_dir = os.path.join(main_dir, run_folder, 'excel\\convert_script.py')

vtk_path  = os.path.join(main_dir, run_folder, 'streamline_pp.vtk')
vtk_path = vtk_path.replace('\\','/')
script_content = "from paraview.simple import *\nreader = OpenDataFile('" + vtk_path + "')\nSaveData('"+ destruct_file + "', proxy=reader, Precision=10)"


def run_pvpython():
    subprocess.run([pvpython_path, script_dir], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text = 'TRUE')

if not os.path.exists(destruct_file): #check if destruct.csv exists
    print('No destruct.csv, creating now') #if not, create it
    if not os.path.exists(script_dir): #check if convert_script.py exists
        print('No convert_script.py, creating now') #if not, create it
        with open(script_dir, "w") as file: #write script to convert vtk to csv
                file.write(script_content)
    else: #if convert_script.py already exists, run pvpython
        print('convert_script.py already exists, skipping creation')
        run_pvpython()
else: #if destruct.csv already exists, skip creation
    print('Destruct.csv already exists, skipping creation')