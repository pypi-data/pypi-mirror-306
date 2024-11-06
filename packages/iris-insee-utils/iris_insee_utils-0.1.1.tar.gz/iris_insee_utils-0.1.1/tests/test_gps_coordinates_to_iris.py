"""This module tests that GPS coordinates are linking to the correct IRIS."""

import pandas as pd

from iris_insee_utils.gps_coordinates_to_iris import gps_to_iris, df_gps_to_iris, gps_to_code_iris



def test_gps_to_iris():
    """
    Test that a single GPS point outputs the correct IRIS.
    """
    result_df = gps_to_iris(5.36413, 43.23871)
    assert result_df.CODE_IRIS.values[0] == "132080302"


def test_gps_to_code_iris():
    """
    Test that a single GPS point outputs the correct IRIS number.
    """
    result_str = gps_to_code_iris(5.362223663076667, 43.41522600589665, 2018)
    assert result_str == "130710101"

def test_df_gps_to_iris():
    """
    Test that GPS points in a DataFrame output the correct IRIS.
    """
    df = pd.DataFrame(
        {
            "Lieu": ["Mairie de Marseille", "Site-Mémorial du Camp des Milles"],
            "longitude": [5.369905252590892, 5.382786610618382],
            "latitude": [43.296630332564405, 43.5034655315141],
        }
    )
    result_df = df_gps_to_iris(df, "longitude", "latitude")
    assert result_df.CODE_IRIS.values[0] == "132020301"
    assert result_df.CODE_IRIS.values[1] == "130010905"


if __name__ == "__main__":
    test_gps_to_iris()
    test_df_gps_to_iris()
    print("All tests passed.")
