## Project Personal - Analysis of the Snow temporal and spatial cover in Rovaniemi, Lapland  using EO Sentinel L2A Data
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Librairies 
from credits import client_id, client_key
from data.Sentinel_data_loading import data_loading
from EDA.number_of_acquisitions import number_of_acquisitions
from EDA.EDA import EDA_form_relation
from preprocessing.preprocessing import preprocessing, preprocessing_ERA5

import sys
import numpy as np
import xarray as xr
import pandas as pd 
from IPython.display import display
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Sentinel data loading: 2017->2026
spatial_rovaniemi =  {"west": 25.7,"south": 66.48,"east": 25.75,"north": 66.52}
bands = ["B03", "B11", "SCL"]

# for k in np.linspace(2017,2025,9):
#     y_start = int(k)
#     y_end = y_start+1
#     start = f"{y_start}-11-01"
#     end = f"{y_end}-04-30"
#     temp = [start, end]
#     print(f"---Winter {temp}---")
#     data_loading(Client_ID=client_id, Client_key=client_key, spatial= spatial_rovaniemi, temporal= temp, bands=bands)
    
#--------------------------------------------------------------------------------------------------------------------------------------------------
# EDA: 
#     0. number of acquisitions
# print(number_of_acquisitions(2017,2025))

#Loop on each Sentinel NetCDF file
cnt = 0
for k in np.linspace(2017,2025,9):
    k = int(k)
    ds = xr.open_dataset(f"C:\\Users\\l.ruizlozano\\Documents\\Project-Sentinel_data\\Rovaniemi\\data\\NetCDF\\L2A_Rovaniemi_winter_{k}_{k+1}.nc")
    #Convert to DataFrame
    df = ds.to_dataframe().reset_index()
    #Concat to a single DataFrame
    if cnt < 1:
        df_Sentinel = df.copy()
        cnt += 1
    else:
        df_Sentinel = pd.concat([df_Sentinel, df])
    

#   1. Information on initial data
shape, info, describe, pd_metric, mask_cloud = EDA_form_relation(df_Sentinel, r'C:\Users\l.ruizlozano\Documents\Project-Sentinel_data\Rovaniemi\figures\EDA\metric_and_relations')
display(pd_metric)
    
#   2.0 Pre processing
df_Sentinel_preprocessed, df_Sentinel_daily_agg = preprocessing(df_Sentinel, mask_cloud)
df_Sentinel_preprocessed.to_csv(r"C:\Users\l.ruizlozano\Documents\Project-Sentinel_data\Rovaniemi\df_Sentinel_silver.csv", index=False)

    
# 2.1 EDA & Pre processing ERA5
url = r'C:\Users\l.ruizlozano\Documents\Project-Sentinel_data\Rovaniemi\data\NetCDF\data_stream-oper_stepType-accum.nc'
ds = xr.open_dataset(url)
df_accum = ds.to_dataframe().reset_index() #precipitation

url = r'C:\Users\l.ruizlozano\Documents\Project-Sentinel_data\Rovaniemi\data\NetCDF\data_stream-oper_stepType-instant.nc'
ds = xr.open_dataset(url)
df_inst = ds.to_dataframe().reset_index() # skin temp, snow depth

df_ERA5_merged_feature, df_ERA5_merged = preprocessing_ERA5(df1=df_accum, df2=df_inst)
# Merge Sentinel and ERA5 data 
df_Sentinel_ERA5 = pd.merge(df_Sentinel_daily_agg,df_ERA5_merged_feature, on = "t", how ="inner" )
df_Sentinel_ERA5.to_csv(r"C:\Users\l.ruizlozano\Documents\Project-Sentinel_data\Rovaniemi\df_Sentinel_ERA5_gold.csv", index=False)
df_Sentinel_ERA5_ML = pd.merge(df_Sentinel_daily_agg,df_ERA5_merged, on = "t", how ="inner" ) 
df_Sentinel_ERA5_ML.to_csv(r"C:\Users\l.ruizlozano\Documents\Project-Sentinel_data\Rovaniemi\df_Sentinel_ERA5_ML_gold.csv", index=False)
#--------------------------------------------------------------------------------------------------------------------------------------------------
# Feature analysis: see Notebook features_analysis for time series and visualisation

#--------------------------------------------------------------------------------------------------------------------------------------------------
# Machine Learning

#--------------------------------------------------------------------------------------------------------------------------------------------------
# Deep Learning
#--------------------------------------------------------------------------------------------------------------------------------------------------
print('--- Job done---')

# EXTRA
# Send tables in the DB: bronze, silver, gold
# Push to GitHub