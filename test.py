import tkinter as tk
from tkinter import filedialog
netj_files = filedialog.askopenfilenames(
    title="Select .NETJ files, skip to use previous files",
    filetypes=[("NETJ Files", "*.netj")],
    initialdir='C:/Users/KWILKES/Desktop/PFAS_Modeling/cfs_runs/0000_docs',
    multiple=True
)