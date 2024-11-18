import logging

import xarray as xr
from distributed import Client
from icechunk import (
    IcechunkStore,
    StorageConfig,
    StoreConfig,
    VirtualRefConfig,
)
from virtualizarr.writers.icechunk import dataset_to_icechunk

from virtualize_nex_gddp_cmip6.inventory import get_uris
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


def store_virtual_dataset(vds: xr.Dataset, name: tuple[str, str, str, str]) -> None:
    """Store virtual dataset in a icechunk virtual reference store

    Args:
        vds (xr.Dataset): virtual dataset
        name (tuple[str, str, str, str]): group name in the form of (GCM, scenario, model, variable)
    """
    storage = StorageConfig.s3_from_env(
        bucket="nasa-veda-scratch",
        prefix=f"virtualizarr-test/maxrjones/{name[0]}/{name[1]}/{name[2]}/{name[3]}",
    )
    config = StoreConfig(
        virtual_ref_config=VirtualRefConfig.s3_anonymous(),
    )
    virtual_store = IcechunkStore.open_or_create(storage=storage, config=config, mode="w")
    dataset_to_icechunk(vds, virtual_store)
    virtual_store.commit("Create refenence dataset")


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
