import xarray as xr
from icechunk import (
    IcechunkStore,
    StorageConfig,
    StoreConfig,
    VirtualRefConfig,
)
from virtualizarr.writers.icechunk import dataset_to_icechunk


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
