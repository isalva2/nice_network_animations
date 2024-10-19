from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np


def horizontal_wave(gdf, frames:int = 10, epsg=3435):
    """
    Strips all attribute information from GeoDataFrame and
    adds animation. This one is a sine wave
    """

    # crs conversion from WGS 84, Illinois Default for now
    # and get x, y geometries for sine wave values
    gdf = gdf.to_crs(f"epsg:{epsg}")
    gdf["centroid"] = gdf.geometry.centroid
    gdf["x_center"] = gdf.centroid.x
    gdf["y_center"] = gdf.centroid.y

    # return GeoDataFrame for plotting
    animation_gdf = gdf.loc[:,["x_center", "y_center","geometry"]]


    # plot on x vals, get range of x
    minx, _, maxx, _ = animation_gdf.total_bounds
    range_x = maxx - minx

    # sine wave loop
    for step in range(0, frames):
        col_name = f"t_{step}"

        # compute sine wave values
        x_vals = animation_gdf["x_center"].values
        y_vals = _step_sine(x_vals, minx, maxx, phase_step = step)

        # write back to gdf
        animation_gdf[col_name] = y_vals

    # drop everything except for animation frames and geometry
    keep_cols = [col for col in animation_gdf.columns if col.startswith("t")] + ["geometry"]
    animation_gdf = animation_gdf[keep_cols]

    return animation_gdf


def _step_sine(x, minx: float, maxx: float, n_periods:int = 5, steps:int=10, phase_step:int=0) -> float:
    range_x = maxx - minx
    frequency = (2 * np.pi * n_periods) / range_x

    phase = 2 * np.pi / steps
    sine_val = 0.5 * np.sin(frequency * (x - minx) + phase * phase_step) + 0.5
    return sine_val
