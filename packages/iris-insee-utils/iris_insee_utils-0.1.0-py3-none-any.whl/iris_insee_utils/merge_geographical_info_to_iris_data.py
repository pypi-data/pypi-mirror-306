"""This module provide functions to enrich data with gps info (e.g. real estates transactions),
with data at the iris level (e.g. poverty rate in an IRIS),
by using IGN geographical dat to join the two datasets.
"""

import pandas as pd
import geopandas as gpd

from iris_insee_utils.gps_coordinates_to_iris import df_gps_to_iris


def merge_gps_dataset_to_iris_dataset(
    df_oi: pd.DataFrame,
    df_enrich: pd.DataFrame,
    iris_year: int = 2018,
    iris_full_info: bool = False,
    df_oi_longlat_colname: tuple[str, str] = (
        "longitude",
        "latitude",
    ),  # TODO: transform to kwargs.
    df_enrich_iriscol_colname: str = None,
) -> gpd.GeoDataFrame:
    """
    Merge the dataset of interest that contains GPS information for each row,
    with another dataset that contains data at the IRIS level.

    Suggested usage: rename the columns of the datasets to 'longitude' and 'latitude' before using this function.

    Parameters
    ----------
    df_oi : pd.DataFrame
        DataFrame containing the dataset of interest with GPS information.
    df_enrich : pd.DataFrame
        DataFrame containing the dataset with IRIS level data to enrich the dataset of interest.
    iris_year : int, optional
        Year of the IRIS data to use. Default is 2018.
    iris_full_info : bool, optional
        If True, return the full information of the IRIS (name, etc.). Default is False.
    df_oi_longlat_colname : tuple[str, str], optional
        Tuple containing the column names for longitude and latitude in the dataset of interest. Default is ('longitude', 'latitude').
    df_enrich_iriscol_colname : str, optional
        Column name in the enrichment dataset that contains the IRIS codes. Default is None.

    Returns
    -------
    geopandas.GeoDataFrame
        A GeoDataFrame with the merged data, containing the original dataset of interest enriched with IRIS level data.

    Examples
    --------
    >>> df_oi = pd.DataFrame({
    ...     'Lieu': ['Mairie de Marseille', 'Site-Mémorial du Camp des Milles'],
    ...     'longitude': [5.369905252590892, 5.382786610618382],
    ...     'latitude': [43.296630332564405, 43.5034655315141]
    ... })
    >>> df_enrich = pd.DataFrame({
    ...     'CODE_IRIS': ['130550101', '130010101'],
    ...     'Some_IRIS_Data': [100, 200]
    ... })
    >>> merge_gps_dataset_to_iris_dataset(df_oi, df_enrich, 2018, False, ('longitude', 'latitude'), 'CODE_IRIS')
    Out[11]: 
                        geometry  index_right INSEE_COM  ...  CODE_IRIS              NOM_IRIS TYP_IRIS
    0  POINT (5.36222 43.41523)        37408     13071  ...  130710101  Cd6-Plan de Campagne        A
    """

    df_oi_iris = df_gps_to_iris(
        df_oi,
        df_oi_longlat_colname[0],
        df_oi_longlat_colname[1],
        iris_year=iris_year,
        iris_full_info=iris_full_info,
    )

    df_enrich = df_enrich.astype({df_enrich_iriscol_colname: "str"})
    print(df_oi_iris)

    return pd.merge(
        df_oi_iris.astype({"CODE_IRIS": "str"}),
        df_enrich,
        left_on="CODE_IRIS",
        right_on=df_enrich_iriscol_colname,
    )
