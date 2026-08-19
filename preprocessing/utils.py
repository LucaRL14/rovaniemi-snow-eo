from pyproj import Transformer

def convert_spatial_coordinates(df: object):
    '''
    *Inputs*
    - df: pd DataFrame
    *Outputs*
    - df with lat, lon columns: geographic latitude and longitude [°]
    '''

    # Transformer UTM35N -> WGS84 (lat/lon)
    transformer = Transformer.from_crs(
        "EPSG:32635",
        "EPSG:4326",
        always_xy=True
    )

    # Conversion
    df['lon'], df['lat'] = transformer.transform(df['x'].values,
                                                df['y'].values)
    
    return df

def cloud_masking(df: object, mask_cloud: bool):
    '''
    Cloud detection and masking per pixel.
    *Inputs*
    - df: DataFrame
    - mask_cloud: bool
    *Output*
    - df_cloudless; DataFrame without cloudy pixels
    '''
    
    df_cloudless = df[~mask_cloud]
    return df_cloudless


def NDSI(df: object):
    '''
    Computes the Normalised Difference Snow Index (NDSI). 
    See: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/ndsi/
    
    *Input*
    - df: pd DataFrame
    *Output*
    - df_copy: df with NDSI column
    '''
    df_copy = df.copy()
    ndsi = (df_copy["B03"] - df_copy["B11"]) / (df_copy["B03"] + df_copy["B11"])
    df_copy["NDSI"] = ndsi
    return df_copy


def temporale_aggregate(df: object):
    
    pass