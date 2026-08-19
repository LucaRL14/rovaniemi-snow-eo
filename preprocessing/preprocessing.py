import seaborn as sns 
import matplotlib.pyplot as plt
from pathlib import Path
import scipy.stats as sc
import pandas as pd 
import numpy as np 
from .utils import convert_spatial_coordinates, cloud_masking, NDSI
def preprocessing(df: object, mask_cloud: bool):
    '''
    Pre-processing of the Sentinel DataFrame:
    - convert the projected coordinates x,y to longitude, latitude
    - add time columns: year, month, day, DOY
    - remove redondant and unuseful columns: 'x', 'y', 'crs'
    - mask the cloudy pixels
    - compute the NDSI
    - Daily aggregate and snow fraction
    
    *Input*
    - df: DataFrame
    - mask_cloud: bool
    -# k: year
    *Output*
    - df_preprocessed: pre processed DataFrame
    - df_agg: daily aggregate df_preprocessed
    
    '''
    
    df = convert_spatial_coordinates(df)
    
    # Add time columns and DOY
    df['year'] = df['t'].dt.year
    df['month'] = df['t'].dt.month
    df['day'] = df['t'].dt.day
    df['DOY'] = df['t'].dt.dayofyear
    
    # Remove x, y, crs col
    df = df[["t", "year", "month", "day", "DOY", "lon","lat","B03", "B11", "SCL"]]
    
    # Mask cloudy pixels
    df_cloudless = cloud_masking(df, mask_cloud)
    
    # Remove NaN values: in this case <1%, all in the same acquisition
    df_clean =  df_cloudless.dropna(subset=["B03","B11","SCL"])
    
    # NDSI
    df_preprocessed = NDSI(df_clean)
    
    # Fig histo NDSI
    # figname = f"hist_NDSI_winter_{k}_{k+1}.png"
    figname = "hist_NDSI_winter_2017_2026.png"
    figpath= r'C:\Users\l.ruizlozano\Documents\Project-Sentinel_data\Rovaniemi\figures\pre_processing'
    outfile = Path(figpath) / figname
    
    # plt.figure()
    # ax = sns.histplot(data=df_preprocessed, x = df_preprocessed["NDSI"], bins=30)
    # ymax = ax.get_ylim()[1]
    # plt.xlim([0,1])
    # plt.vlines(x=0.42, ymin=0, ymax= ymax , colors="black", linestyles='--', label='Snow threshold')
    # plt.legend()
    # plt.title(f"Winter {k}-{k+1}")
    # plt.savefig(outfile)
    # plt.figure()
    # ax = sns.histplot(data=df_preprocessed, x = df_preprocessed["NDSI"], bins=30)
    # ymax = ax.get_ylim()[1]
    # plt.xlim([0,1])
    # plt.vlines(x=0.42, ymin=0, ymax= ymax , colors="black", linestyles='--', label='Snow threshold')
    # plt.legend()
    # plt.title(f"Winter 2017-2026")
    # plt.savefig(outfile)

    # Daily aggregate
    df_agg = df_preprocessed.groupby("t").agg(
                                                year=("year", "min"),
                                                month=("month", "min"),
                                                day=("day", "min"),
                                                DOY=("DOY", "min"),
                                                ndsi_median=("NDSI", "median"),
                                                ndsi_mad=("NDSI", lambda x: sc.median_abs_deviation(x)),
                                                snow_fraction=("NDSI", lambda x: (x > 0.42).mean())
                                            )
    return df_preprocessed, df_agg


def preprocessing_ERA5(df1: object, df2: object):
  '''
  Pre-processing of the ERA5 DataFrame:
    - Merge both objects keeping: total precipitation tp [mm], skin temperature skt [°C], snow depth sd [cm]
    - Drop rows with datetime < 2017-12-01, not matching Sentinel observations
    - Compute winter season time
    - Add season time columns
    
    *Input*
    - df1: DataFrame
    - df2: DataFrame

    *Output*
    - df: pre processed DataFrame for feature analysis
    - df_merged:  pre processed DataFrame. Distance/depth/column units are in [m]
  '''
  df_merged = pd.merge(df1, df2, on="valid_time")
  df_merged = df_merged[['valid_time', 'tp', 'skt', 'sd']]
  df_merged['valid_time'] = pd.to_datetime(df_merged['valid_time'].dt.date)

  df_merged[df_merged['valid_time'] == '2017-11-01 00:00:00']
  #Drop all data before 2017-11-01
  df_merged = df_merged.drop(df_merged.index[np.where(df_merged.index <480)[0]])
  
  #DataFrame for feature analysis
  df_merged_feature = df_merged.copy()
  df_merged_feature['tp'] = df_merged_feature['tp']*1000 #tp [m]->[mm]
  df_merged_feature['skt'] = df_merged_feature['skt']-273.15 #Kelvin -> Celsius
  df_merged_feature['sd'] = df_merged_feature['sd']*100 # [m]->[cm]
  
  df = df_merged_feature.copy()

  # Winter season starts in Nov
  df['winter_start'] = np.where(
      df['valid_time'].dt.month == 11,
      df['valid_time'].dt.year,
      df['valid_time'].dt.year - 1
  )

  df['winter'] = (
      df['winter_start'].astype(str)
      + '-'
      + (df['winter_start']+1).astype(str)
  )

  # Winter day
  df['winter_day'] = pd.to_datetime(
      '2000-' +
      df['valid_time'].dt.month.astype(str).str.zfill(2) + '-' +
      df['valid_time'].dt.day.astype(str).str.zfill(2)
  )

  # Rescale on a same winter season 
  mask = df['valid_time'].dt.month <= 4
  df.loc[mask, 'winter_day'] += pd.DateOffset(years=1)
  

  df = df.rename(columns={"valid_time":"t"})
  df = df.set_index("t")
  
  df_merged = df_merged.rename(columns={"valid_time":"t"})
  df_merged = df_merged.set_index("t")
  
  return df, df_merged
  
  
    