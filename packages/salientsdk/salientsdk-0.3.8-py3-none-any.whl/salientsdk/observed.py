#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Observed data timeseries.

This module acquires observed station meteorological data and converts it into a format
compatible with the `data_timeseries` function.
"""

from collections.abc import Iterable

import numpy as np
import pandas as pd
import xarray as xr


def make_observed_ds(
    obs_df: pd.DataFrame | str | Iterable[pd.DataFrame | str],
    name: str | Iterable[str],
    variable: str,
    time_col: str = "time",
) -> xr.Dataset:
    """Convert weather observation DataFrame(s) to xarray Dataset.

    This function converts tabular meteorological data into a format identical to
    `data_timeseries(..., frequency='daily') suitable for use with the `crps` function.

    Args:
        obs_df: Single DataFrame or a filename to a CSV that can be read as a dataframe.
            May also be an iterable vector of filenames or `DataFrame`s.
            Each DataFrame should have columns for `time` and the `variable` of interest.
            If the dataframe contains lat, lon, and elev metadata the function will
            preserve thse as coordinates. Function `get_ghcnd` will provide a compatible
            dataset, or you can provide your own.
        name: Station name(s) corresponding to the DataFrame(s). Must be a string if obs_df
            is a single DataFrame, or an iterable of strings matching the length of obs_df
            if multiple DataFrames are provided.
        variable: Name of the column in obs_df to extract the met data (e.g. 'temp', 'precip').
        time_col: Name of the column in obs_df containing the time (default `time`)

    Returns:
        xarray Dataset containing the variable data and station metadata. Has dimensions
        'time' and 'location', with coordinates for station lat/lon/elevation.
    """
    """
    examples assume the existence of get_ghcnd, which is found in validate.ipynb:
    Examples:
        Single station:
        >>> ds = make_observed_ds(
        ...     obs_df=get_ghcnd("USW00013874"),
        ...     name="ATL",
        ...     variable="temp"
        ... )

        Multiple stations:
        >>> ds = make_observed_ds(
        ...     obs_df=get_ghcnd(["USW00013874", "USW00014739"]),
        ...     name=["ATL", "BOS"],
        ...     variable="temp"
        ... )
    """
    if isinstance(obs_df, Iterable) and not isinstance(obs_df, pd.DataFrame):
        if name is None or isinstance(name, str):
            raise ValueError(
                "When obs_df is a list of DataFrames, name must be an iterable of strings"
            )

        assert len(obs_df) == len(
            name
        ), f"Length mismatch: got {len(obs_df)} DataFrames but {len(name)} names"

        ds = [
            make_observed_ds(obs_df=df, name=n, variable=variable) for df, n in zip(obs_df, name)
        ]
        return xr.concat(ds, dim="location")

    if isinstance(obs_df, str):
        obs_df = pd.read_csv(obs_df)

    name = str(name)

    ds = xr.Dataset(
        data_vars={
            "vals": (("time", "location"), obs_df[variable].values[:, np.newaxis]),
        },
        coords={
            "time": pd.to_datetime(obs_df[time_col]),
            "location": [name],
        },
    )
    ds.attrs["short_name"] = variable

    # Transfer metadata attributes if they exist
    if hasattr(obs_df[variable], "attrs"):
        for attr in ["units", "long_name"]:
            if attr in obs_df[variable].attrs:
                ds.attrs[attr] = obs_df[variable].attrs[attr]

    # Preserve station geo-coordinates if they exist as a column (per ghcnd, for example)
    for coord in ["lat", "lon", "elev"]:
        if coord in obs_df.columns:
            ds = ds.assign_coords({f"{coord}_station": ("location", [obs_df[coord].mean()])})

    return ds
