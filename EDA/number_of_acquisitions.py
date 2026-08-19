import numpy as np 
import pandas as pd 
import xarray as xr
import matplotlib.pyplot as plt
from pathlib import Path

def number_of_acquisitions(start_y: int, end_y: int)->int:
    '''
    This function returns the number of Sentinel-2 acquisitions over the selected area et period.
    
    *Inputs*
    - start_y: year 1
    - end_y: year 2
    - filename: NetCDF file
    
    *Ouput*
    - cnt: total number of acquisitions
    - figures
    '''
    cnt = 0
    delta_y = (end_y-start_y)+1
    for k in np.linspace(start_y,end_y,delta_y):
        k = int(k)
        filepath = f"C:\\Users\\l.ruizlozano\\Documents\\Project-Sentinel_data\\Rovaniemi\\data\\NetCDF\\L2A_Rovaniemi_winter_{k}_{k+1}.nc"
        ds = xr.open_dataset(filepath)
        cnt += ds.t.shape[0]
        print(f'---Winter {k}-{k+1}---')
        print(f'- Number of acquisitions: {ds.t.shape[0]}')
        
        #Figures
        dates = pd.to_datetime(ds.t.values)
        figpath = r'C:\Users\l.ruizlozano\Documents\Project-Sentinel_data\Rovaniemi\figures\EDA\number_of_acquisitions'
        figname = f"acquisitions_{filepath[-19:-3]}.png"
        outfile = Path(figpath) / figname
        plt.figure()
        plt.eventplot(dates)
        plt.yticks([])
        plt.xlabel('Date')
        plt.xticks(rotation=45)
        plt.title('Sentinel-2 acquisition dates: Rovaniemi')
        plt.savefig(outfile)
    
    print(f'Figures saved in: {figpath}')
    print('---Total acquisitions---')
    return cnt