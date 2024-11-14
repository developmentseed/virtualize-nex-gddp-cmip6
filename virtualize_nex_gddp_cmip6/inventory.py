"""
The NASA NEX-GDDP-CMIP6 dataset on AWS is comprised of over 100,000 NetCDF files, which are indexed in a few text files in https://nex-gddp-cmip6.s3.us-west-2.amazonaws.com/index.html.
"""

from typing import Literal

import pandas as pd


def get_inventory(version: Literal["1.0", "1.1", "1.2"]) -> pd.DataFrame:
    """Get all file URIs for a given version of the NEX-GDDP-CMIP6 dataset, based on the index file.

    Args:
        version (Literal['1.0', '1.1', '1.2']): Version of the dataset to index.

    Returns:
        pd.DataFrame: Dataframe containing metadata and URIs of all NetCDF files for that version.
    """
    file = "index_md5.txt" if version == "1.0" else f"index_v{version}_md5.txt"
    df = pd.read_csv(
        f"https://nex-gddp-cmip6.s3-us-west-2.amazonaws.com/{file}", sep=r"\s+", header=None, names=["shasum", "path"]
    )
    df = pd.read_csv(
        f"https://nex-gddp-cmip6.s3-us-west-2.amazonaws.com/{file}", sep=r"\s+", header=None, names=["shasum", "path"]
    )
    df[["bucket", "GCP", "scenario", "model", "variable", "file"]] = df["path"].str.split("/", expand=True)
    df["uri"] = "s3://nex-gddp-cmip6/" + df["path"]
    df["file"] = df["file"].str.replace(".nc", "").str.replace("_v1.1", "").str.replace("_v1.2", "")
    df["version"] = version
    return df.set_index("file")


def get_uris() -> list:
    """Get a dataframe containing file URIs for the latest releases of the NASA NEX-GDDP-CMIP6 data.

    Returns:
        pd.DataFrame: Dataframe containing metadata and URIs for all NetCDF files. The URI of the latest version is provided for datasets with multiple versions.
    """
    df = get_inventory("1.0")
    df.update(get_inventory("1.1"))
    df.update(get_inventory("1.2"))
    return df
