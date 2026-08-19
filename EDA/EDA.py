import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def EDA_form_relation(df: object, figpath: str):
    '''
    Returns the general information of the dataset and the metrics.
    *Input*
    - pd_df: pandas.DataFrame
    - #k: year
    - figpath: path where to save figures
    *Outputs*
    - shape: of the dataset
    - info: of the dataset
    - describe: metric of numerical columns
    - pd_metric: DataFrame of data quality
    - mask_cloud: boolean given cloudy pixels
    
    '''
    #---EDA form analysis---
    #General information
    shape = df.shape
    info = df.info()
    describe = df.describe()
    
    #Data quality and metrics
    mask_nan = (df['SCL'] == 0)
    mask_bad = (df['SCL'] == 1)
    mask_cloud = df['SCL'].isin([3,7,8,9,10])

    dict = {"Metric": ["Total pixels", "NaN", "Bad pixels","Cloudy pixels"],
            "Total": [len(df), mask_nan.sum(), mask_bad.sum(), mask_cloud.sum()],
            "Percentage": [100, mask_nan.mean()*100, mask_bad.mean()*100, mask_cloud.mean()*100]
            }
    pd_metric = pd.DataFrame(data=dict)
    
    #---EDA relation analysis---
    # for c in ["B03", "B11"]:
    #     # figname = f"hist_{c}_winter_{k}_{k+1}.png"
    #     # outfile = Path(figpath) / figname
        
    #     # plt.figure()
    #     # #plt.hist(df[c], bins=30)
    #     # sns.histplot(data=df, x = df[c], bins=30)
    #     # plt.title(f"Winter {k}-{k+1}")
    #     # plt.savefig(outfile)
    #     figname = f"hist_{c}_winter_2017_2026.png"
    #     outfile = Path(figpath) / figname
        
    #     plt.figure()
    #     #plt.hist(df[c], bins=30)
    #     sns.histplot(data=df, x = df[c], bins=30)
    #     plt.title("Winter 2017-2026")
    #     plt.savefig(outfile)
    
    # #Correlation matrice
    # mat_corr =df.corr(numeric_only=True)
    # figname = f"corr_{c}_winter_2017_2026.png"
    # outfile = Path(figpath) / figname
    
    # plt.figure(figsize=(10, 8))
    # sns.heatmap(mat_corr, annot=True, cmap="coolwarm", linewidths=0.5)
    # plt.title(f"Correlation Matrix: Winter ")
    # plt.savefig(outfile)
    # print(f"Figures saved in: {Path(figpath) }")
    
    return shape, info, describe, pd_metric, mask_cloud
    
    
def EDA_ERA5(df: object, figpath: str):
    '''
    Returns the general information of the ERA5 dataset and the metrics.
    *Input*
    - df: pandas.DataFrame
    - figpath: path where to save figures
    *Outputs*
    - shape: of the dataset
    - info: of the dataset
    - describe: metric of numerical columns
    - pd_metric: DataFrame of data quality
    '''
    #---EDA form analysis---
    #General information
    shape = df.shape()
    info = df.info()
    describe = df.describe()
    null_count = df.isna().sum()
    
    return shape, info, describe, null_count