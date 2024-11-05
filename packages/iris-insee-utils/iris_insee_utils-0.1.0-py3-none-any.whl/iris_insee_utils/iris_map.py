"""This module is for plotting IRIS data."""

import os

from iris_insee_utils.get_iris_contours_data import read_or_download_iris_contour_data
from iris_insee_utils.gps_coordinates_to_iris import gps_to_iris
import pandas as pd
from loguru import logger
import geopandas as gpd
import folium
from tqdm import tqdm
import numpy as np

from loguru import logger


def plot_folium_map(
    iris_year,
    commune_name="Marseille",
    df_oi: pd.DataFrame = None,
    df_enrich: pd.DataFrame = None,
    df_enrich_iriscol_colname=None,
    df_enrich_select_cols=None,
    save_map_path=None,
):
    """
    Plot a folium map of IRIS (Ilots Regroupés pour l'Information Statistique) for a given commune or department number.
                    Parameters
                    ----------
                    iris_year : int
                        The year of the IRIS data to be used.
                    commune_name : str, optional
                        The name of the commune to filter the IRIS data, by default "Marseille".
                    df_oi : pd.DataFrame, optional
                        A DataFrame containing points of interest with latitude and longitude columns, by default None.
                    df_enrich : pd.DataFrame, optional
                        A DataFrame containing additional data to enrich the IRIS data, by default None.
                    df_enrich_iriscol_colname : str, optional
                        The column name in `df_enrich` that corresponds to the IRIS code, by default None.
                    df_enrich_select_cols : list, optional
                        A list of columns in `df_enrich` to be included in the map, by default None.
                    save_map_path : str, optional
                        Absolute path where the map will be saved to an HTML file, by default None.
                    Returns
                    -------
                    folium.Map
                        A Folium map object with the plotted IRIS data and optional points of interest.
                    Raises
                    ------
                    NotImplementedError
                        If `save_map` is True, as this functionality has not been implemented yet.
                    Notes
                    -----
                    - The function reads a parquet file containing IRIS data for the specified year.
                    - The IRIS data is filtered by the specified commune name.
                    - If `df_enrich` is provided, it merges the IRIS data with the enrichment data.
                    - If `df_oi` is provided, it adds markers for points of interest to the map.
                    - The map is centered on the centroid of the filtered IRIS geometries.
                    - The map is returned as a Folium map object.
    """

    df_map = read_or_download_iris_contour_data(iris_year).to_crs(
        epsg=4326
    )  # TODO: add this to the cleaning function
    df_map["NOM_COM"] = (
        df_map.NOM_COM.str.strip()
    )  # remove leading and trailing spaces, TODO: add this to the cleaning function
    df_map = df_map[
        df_map.NOM_COM.str.contains(commune_name, case=True)
    ]  # df_map = df_map.query("NOM_COM == @commune_name")
    m = folium.Map(
        location=[df_map.geometry.centroid.y.mean(), df_map.geometry.centroid.x.mean()],
        zoom_start=12,
    )

    if df_enrich is not None:
        df_enrich = df_enrich.astype({df_enrich_iriscol_colname: "str"})
        df_map = pd.merge(
            df_map.astype({"CODE_IRIS": "str"}),
            df_enrich.loc[:, df_enrich_select_cols + [df_enrich_iriscol_colname]],
            left_on="CODE_IRIS",
            right_on=df_enrich_iriscol_colname,
        )

    for _, row in df_map.iterrows():
        enrich_iris_info = ""
        if df_enrich is not None:
            for column_name, value in row.items():

                if column_name in df_enrich_select_cols:
                    enrich_iris_info += f"{column_name}: {np.round(value,2)}<br>"

        sim_geo = gpd.GeoSeries(row["geometry"])  # .simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(
            data=geo_j,
            smooth_factor=0.1,
            style_function=lambda x: {"fillColor": "lightblue"},
        )
        iris_base_info = (
            "Code iris: "
            + row["CODE_IRIS"]
            + "<br>"
            + "nom iris: "
            + row["NOM_IRIS"]
            + "<br>"
            + "Commune: "
            + row["NOM_COM"]
            + "<br>"
        )
        folium.Popup(iris_base_info + enrich_iris_info).add_to(geo_j)
        geo_j.add_to(m)

    if df_oi is not None:

        for _, row in df_oi.iterrows():
            location = [row["lat"], row["lon"]]
            tooltip = ""
            for column_name, value in row.items():
                if column_name not in ["lat", "lon"]:
                    tooltip += f"{column_name}: {value}<br>"

            m.add_child(
                folium.Marker(
                    location=[row["lat"], row["lon"]], tooltip=tooltip  # icon=icon,
                )
            )
    if save_map_path is not None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"Saving map to {save_map_path}")
        m.save(save_map_path)

    return m


if __name__ == "__main__":
    plot_folium_map(iris_year=2018, commune_name="Nice")
