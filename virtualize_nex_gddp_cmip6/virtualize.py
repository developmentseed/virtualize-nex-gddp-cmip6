import dask
import xarray as xr
from dask.delayed import Delayed
from virtualizarr import open_virtual_dataset


def generate_virtual_dataset(file: str, storage_options: dict) -> xr.Dataset:
    return open_virtual_dataset(file, indexes={}, reader_options={"storage_options": storage_options})


def generate_tasks(uris: list[str]) -> list[Delayed]:
    storage_options = {"anon": True, "default_fill_cache": False, "default_cache_type": "first"}
    tasks = [dask.delayed(generate_virtual_dataset)(file, storage_options) for file in uris]
    return tasks


def execute_tasks(tasks: list[Delayed]) -> list[xr.Dataset]:
    return list(dask.compute(*tasks))


def combine_virtual_datasets(virtual_datasets: list[xr.Dataset]) -> xr.Dataset:
    return xr.concat(virtual_datasets, dim="time", coords="minimal", compat="override")
