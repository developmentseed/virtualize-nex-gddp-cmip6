import dask
import xarray as xr
from dask.delayed import Delayed
from virtualizarr import open_virtual_dataset


def generate_virtual_dataset(file: str, storage_options: dict) -> xr.Dataset:
    """Generate a virtual dataset for a NetCDF file

    Args:
        file (str): Dataset URI
        storage_options (dict): Options to pass through to fsspec for reading the dataset

    Returns:
        xr.Dataset: virtual dataset containing metadata and data references
    """
    return open_virtual_dataset(file, indexes={}, reader_options={"storage_options": storage_options})


def generate_tasks(uris: list[str]) -> list[Delayed]:
    """Generate dask delayed objects to parallelize virtual dataset creation

    Args:
        uris (list[str]): URIs for all files that should be virtualized

    Returns:
        list[Delayed]: List of dask delayed objects for virtualized datasets
    """
    storage_options = {"anon": True, "default_fill_cache": False, "default_cache_type": "first"}
    tasks = [dask.delayed(generate_virtual_dataset)(file, storage_options) for file in uris]
    return tasks


def execute_tasks(tasks: list[Delayed]) -> list[xr.Dataset]:
    """Execute tasks for creating virtual datasets

    Args:
        tasks (list[Delayed]): Dask delayed objects for virtual dataset generation

    Returns:
        list[xr.Dataset]: List of virtual datasets
    """
    return list(dask.compute(*tasks))


def combine_virtual_datasets(virtual_datasets: list[xr.Dataset]) -> xr.Dataset:
    """
    Combine many virtual datasets into a single dataset by concatenating over the time dimension

    Datasets are expected to be in the correct order in the input list and have matching non-time dimensions/coordinates.

    Args:
        virtual_datasets (list[xr.Dataset]): List of virtual datasets

    Returns:
        xr.Dataset: Concatenated virtual dataset
    """
    return xr.concat(virtual_datasets, dim="time", coords="minimal", compat="override")
