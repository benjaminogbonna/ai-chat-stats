import os
import pytz
import json
import zipfile
from datetime import datetime, timezone, timedelta

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


def clac_convo_times(data, ltz):
    with open(f'{data}', 'r') as f:
                convs = json.load(f)
    convo_times = []
    for conv in convs:
            # Given Unix timestamp
            unix_timestamp = conv['create_time']
            # Convert to UTC datetime
            utc_datetime = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
            # Convert UTC datetime to local timezone
            pt_datetime = utc_datetime.astimezone(pytz.timezone(ltz))
            convo_times.append(pt_datetime)

    return convo_times

