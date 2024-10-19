from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point


def horizontal_wave(gdf, frames:int = 10, epsg = 3435, n_periods = 3) -> gpd.GeoDataFrame:
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
        y_vals = _step_sine(x_vals, minx, maxx, phase_step = step, n_periods=n_period)

        # write back to gdf
        animation_gdf[col_name] = y_vals

    # drop everything except for animation frames and geometry
    keep_cols = [col for col in animation_gdf.columns if col.startswith("t")] + ["geometry"]
    animation_gdf = animation_gdf[keep_cols]

    return animation_gdf


def spider_wave(gdf, frames:int = 10, epsg=3435, center="Chicago", n_periods = 3) -> gpd.GeoDataFrame:
    """
    Strips all attribute information from GeoDataFrame and
    adds animation. This one is a radial sine wave, default
    center at Chicago, Il.
    """
    # Default center dict, add more with time.
    # THIS IS IN LON LAT
    center_dict = {
        "Chicago":(-87.630098, 41.881533)
    }

    # get default crs
    crs_wgs84 = gdf.crs
    target_crs = f"epsg:{epsg}"

    # get center from city dict and do crs conversion
    center_gdf = gpd.GeoDataFrame(
        geometry = [Point(center_dict[center])],
        crs = crs_wgs84
    )
    center_gdf = center_gdf.to_crs(target_crs)
    gdf = gdf.to_crs(target_crs)

    # get center coordinate in new crs
    center_coord = (center_gdf.geometry.x.values[0], center_gdf.geometry.y.values[0])

    # get xy coords of every segment
    x_vals = gdf.geometry.centroid.x.values
    y_vals = gdf.geometry.centroid.y.values
    xy_coords = [np.array(pair) for pair in zip(x_vals, y_vals)]

    # get euclidean radial distances from center
    radial_distances = np.array([
        np.linalg.norm(coord - center_coord) for coord in xy_coords
    ])

    # get sine range
    minx, miny, maxx, maxy = gdf.total_bounds
    bottom_left = (minx, miny)
    top_left = (minx, maxy)
    top_right = (maxx, maxy)
    bottom_right = (maxx, miny)
    corners = (bottom_left, top_left, top_right, bottom_right)

    corner_distances = []
    for corner in corners:
        corner_distance = np.linalg.norm(np.array(corner) - center_coord)
        corner_distances.append(corner_distance)
    max_range = max(corner_distances)

    # sine wave loop
    for step in range(0, frames):
        col_name = f"t_{step}"

        # compute sine wave values
        radial_sine_vals = _step_sine(radial_distances, 0, max_range, phase_step = step, n_periods=n_periods)

        # write back to gdf
        gdf[col_name] = radial_sine_vals

    # drop everything except for animation frames and geometry
    keep_cols = [col for col in gdf.columns if col.startswith("t")] + ["geometry"]
    animation_gdf = gdf[keep_cols]

    return animation_gdf


def _step_sine(x, minx: float, maxx: float, n_periods:int = 5, steps:int=10, phase_step:int=0) -> float:
    range_x = maxx - minx
    frequency = (2 * np.pi * n_periods) / range_x

    phase = 2 * np.pi / steps
    sine_val = 0.5 * np.sin(frequency * (x - minx) + phase * phase_step) + 0.5
    return sine_val
