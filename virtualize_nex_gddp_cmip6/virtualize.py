import dask
import xarray as xr
from virtualizarr import open_virtual_dataset


def generate_virtual_dataset(file, storage_options):
    return open_virtual_dataset(file, indexes={}, reader_options={"storage_options": storage_options})


def generate_tasks(uris):
    storage_options = {"anon": True, "default_fill_cache": False, "default_cache_type": "first"}
    tasks = [dask.delayed(generate_virtual_dataset)(file, storage_options) for file in uris]
    return tasks


def execute_tasks(tasks):
    return list(dask.compute(*tasks))


def combine_virtual_datasets(virtual_datasets):
    return xr.concat(virtual_datasets, dim="time", coords="minimal", compat="override")
