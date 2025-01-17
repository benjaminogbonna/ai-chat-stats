import os
import zipfile

def unzip_data(filename, output_fldr):
    """
    Unzips filename into the current working directory.
    
    Args:
    filename (str): a filepath to a target zip folder to be unzipped.
    """
    
    # Ensure the output folder exists
    os.makedirs(output_fldr, exist_ok=True)
    zip_ref = zipfile.ZipFile(filename, "r")
    zip_ref.extractall(output_fldr)
    zip_ref.close()
