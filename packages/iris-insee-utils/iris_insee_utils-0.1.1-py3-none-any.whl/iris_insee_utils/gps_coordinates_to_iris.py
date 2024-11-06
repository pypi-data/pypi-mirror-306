"""This module provide functions that are related to giving iris information from geographical data."""

import pandas as pd
import geopandas as gpd
from iris_insee_utils.get_iris_contours_data import read_or_download_iris_contour_data
import iris_insee_utils


def gps_to_code_iris(long: float, lat: float, iris_year: int = 2018):
    """
    Get the longitude and latitude of gps point(s), and returns the CODE IRIS.

    Parameters
    ----------
    long : float
        Longitude of the GPS point.
    lat : float
        Latitude of the GPS point.
    iris_year : int, optional
        Year of the IRIS data to use. Default is 2018.

    Returns
    -------
    str
        The CODE IRIS.

    Examples
    --------
    >>> gps_to_code_iris(5.36, 43.41, 2018)
    Out[11]:
    '130710101'
    """
    return gps_to_iris(long, lat, iris_year).CODE_IRIS.values[0]
    

def gps_to_iris(
    long: float, lat: float, iris_year: int = 2018, iris_full_info: bool = False
) -> gpd.GeoDataFrame:
    """
    Get the longitude and latitude of gps point(s), and returns the CODE IRIS.
    More information about TYPE_IRIS can be found here: https://www.insee.fr/fr/information/2438155

    Parameters
    ----------
    long : float
        Longitude of the GPS point.
    lat : float
        Latitude of the GPS point.
    iris_year : int, optional
        Year of the IRIS data to use. Default is 2018.
    iris_full_info : bool, optional
        If True, return the full information of the IRIS (name, ). Default is False.

    Returns
    -------
    geopandas.GeoDataFrame
        A GeoDataFrame with one row containing the CODE IRIS.

    Examples
    --------
    >>> gps_to_iris(5.362223663076667, 43.41522600589665, 2018)
    Out[11]:
           CODE_IRIS           NOM_IRIS    TYP_IRIS
        0  130710101  Cd6-Plan de Campagne        A
    """
    df_ign_map = read_or_download_iris_contour_data(iris_year)
    df_ign_map = df_ign_map.to_crs(epsg=4326)
    gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy([long], [lat]))

    gdf.crs = "EPSG:4326"
    gdf = gdf.to_crs(epsg=4326)
    result_df = gpd.sjoin(gdf.head(1), df_ign_map, predicate="within")
    if iris_full_info:
        return result_df
    return result_df[["CODE_IRIS", "NOM_IRIS", "TYP_IRIS"]]


def df_gps_to_iris(
    df: pd.DataFrame,
    long_col: str,
    lat_col: str,
    iris_year: int = 2018,
    iris_full_info: bool = False,
) -> gpd.GeoDataFrame:
    """
    Get the longitude and latitude from a DataFrame, and returns the CODE IRIS.
    More information about TYPE_IRIS can be found here: https://www.insee.fr/fr/information/2438155

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the GPS points.
    long_col : str
        Name of the column containing the longitude.
    lat_col : str
        Name of the column containing the latitude.
    iris_year : int, optional
        Year of the IRIS data to use. Default is 2018.
    iris_full_info : bool, optional
        If True, return the full information of the IRIS (name, ). Default is False.

    Returns
    -------
    geopandas.GeoDataFrame
        A GeoDataFrame with rows containing the CODE IRIS for each GPS point.

    Examples
    --------
    >>> df = pd.DataFrame({'Lieu':['Mairie de Marseille','Site-Mémorial du Camp des Milles'],'longitude': [5.369905252590892, 5.382786610618382,], 'latitude': [43.296630332564405,43.5034655315141,]})
    >>> df_gps_to_iris(df, 'longitude', 'latitude', 2018)
    Out[11]:
                       geometry  index_right INSEE_COM  ...  CODE_IRIS              NOM_IRIS TYP_IRIS
    0  POINT (5.36222 43.41523)        37408     13071  ...  130710101  Cd6-Plan de Campagne        A
    """
    # Check if the columns are not already in the dataframe
    conflicting_cols = [
        col for col in ["RIS", "NOM_IRIS", "CODE_IRIS"] if col in df.columns
    ]
    assert (
        not conflicting_cols
    ), f"{', '.join(conflicting_cols)} are already in the inputed dataframe columns, please rename them or drop them to avoid conflicts"

    df_ign_map = gpd.read_parquet(
        iris_insee_utils.__path__[0] + f"/../data/transformed/iris_{iris_year}.parquet"
    )
    df_ign_map = df_ign_map.to_crs(epsg=4326)
    df = df.astype(
        {long_col: str, lat_col: str}
    )  # TODO: Check if categorical or string dtype would not be faster or better.
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[long_col], df[lat_col]))

    gdf.crs = "EPSG:4326"
    gdf = gdf.to_crs(epsg=4326)
    result_df = gpd.sjoin(gdf, df_ign_map, predicate="within")
    if iris_full_info:
        return result_df
    return result_df.drop(
        columns=["geometry", "index_right", "INSEE_COM", "NOM_COM", "TYP_IRIS"]
    )
