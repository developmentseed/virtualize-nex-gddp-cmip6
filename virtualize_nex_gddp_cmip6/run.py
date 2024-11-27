import logging

import xarray as xr
from distributed import Client

from virtualize_nex_gddp_cmip6.inventory import get_uris
from virtualize_nex_gddp_cmip6.store import store_virtual_dataset
from virtualize_nex_gddp_cmip6.virtualize import combine_virtual_datasets, execute_tasks, generate_tasks


def execute_dataset_virtualization(uris: list[str]) -> xr.Dataset:
    """Generate a virtual dataset from a list of input data files.

    Args:
        uris (list[str]): list of URIS for NASA NEX-GDDP-CMIP6 data files

    Returns:
        xr.Dataset: virtual dataset containing concatenated chunk manifests
    """
    tasks = generate_tasks(uris)
    virtual_datasets = execute_tasks(tasks)
    vds = combine_virtual_datasets(virtual_datasets)
    return vds


def virtualize():
    """Virtualize the NASA NEX-GDDP-CMIP6 datasets and store in icechunk"""
    df = get_uris()
    # Group input URIs so that output virtual datasets share a GCP, SSP, model, and variable
    grouped = df.groupby(["GCP", "scenario", "model", "variable"])
    for name, group in grouped:
        vds = execute_dataset_virtualization(group["uri"].to_list())
        store_virtual_dataset(vds, name)


if __name__ == "__main__":
    with Client(n_workers=8, silence_logs=logging.ERROR) as client:
        print(client.dashboard_link)
        virtualize()
