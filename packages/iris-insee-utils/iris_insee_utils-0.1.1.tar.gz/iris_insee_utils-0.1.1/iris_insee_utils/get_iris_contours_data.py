"Will get the contour data for the given year by either reading it from cache in data/transformed or by downloading it from iris_insee_utils_data and recording it in data/transformed."
import geopandas as gpd
import iris_insee_utils
import requests
from loguru import logger
from pathlib import Path

def read_or_download_iris_contour_data(iris_year: int) -> gpd.GeoDataFrame:
    """
    Get the contour data for the given year by either reading it from cache in data/transformed or by downloading it from iris_insee_utils_data and recording it in data/transformed.

    Parameters
    ----------
    iris_year : int
        The year of the IRIS data to be used.

    Returns
    -------
    geopandas.GeoDataFrame
        A GeoDataFrame containing the IRIS contour data for the specified year.
    """
    try:
            df_ign_map = gpd.read_parquet(
                iris_insee_utils.__path__[0] + f"/../data/transformed/iris_{iris_year}.parquet"
            )
    except FileNotFoundError:
        logger.info(f"The file iris_{iris_year}.parquet does not exist. Will try to download it and cache it.")
        url = f"https://github.com/adrienpacifico/iris_insee_utils_data/raw/refs/heads/main/data/primary/iris_{iris_year}.parquet"
        response = requests.get(url)
        response.raise_for_status()

        data_dir = Path(iris_insee_utils.__path__[0]).parent / "data" / "transformed"
        data_dir.mkdir(parents=True, exist_ok=True)
        file_path = data_dir / f"iris_{iris_year}.parquet"

        with open(file_path, "wb") as file:
            file.write(response.content)

        df_ign_map = gpd.read_parquet(file_path)
    return df_ign_map

if __name__ == "__main__":   # pragma: no cover
    for year in range(2018, 2024):
        read_or_download_iris_contour_data(iris_year=year)
