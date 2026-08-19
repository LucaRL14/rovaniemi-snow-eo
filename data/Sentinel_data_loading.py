import openeo 
import ssl
from pathlib import Path

def data_loading(Client_ID: str, Client_key: str,spatial: dict, temporal: list, bands: list)-> object:
    '''
This function loads the Sentinel L2A data from the API openeo.
 - => time selection
 - => location selection
 
 *Inputs*
 - Client_ID
 - Client_key
 - spatial: dict
 - temporal: list of str
 - bands: list of str
 
 *Output*
 NetCDF file containing Sentinel L2A data
    '''
    #Force Python to download Natural Earth shapefiles (coastlines)
    ssl._create_default_https_context = ssl._create_unverified_context

    #Connection to the EO API
    link_to_hub = 'https://openeo.dataspace.copernicus.eu'
    connection = openeo.connect(link_to_hub)

    #Authentification
    client_ID  = Client_ID
    client_key = Client_key
    print('---Authenticate with OIDC client credentials---')
    connection.authenticate_oidc_client_credentials(client_ID, client_key)
    print('---Authenticated successfully---')
    
    #Load the Sentinel L2A data: surface reflectance maps
    L2A_datacube = connection.load_collection('SENTINEL2_L2A', 
                                            spatial_extent= spatial,
                                            temporal_extent= temporal,
                                            bands = bands
                                            )
    print('---Connection: OK---')
    #Save NetCDF file
    job = L2A_datacube.create_job(out_format="NetCDF")
    job.start_and_wait()
        
    project_dir = Path(__file__).parent
    output_dir = project_dir / "NetCDF"
    output_dir.mkdir(exist_ok=True)

    file_name = output_dir / f"L2A_Rovaniemi_winter_{temporal[0][:4]}_{temporal[1][:4]}.nc"
    job.download_result(str(file_name))

    print('---')
    print(f"{file_name}: downloaded")
    