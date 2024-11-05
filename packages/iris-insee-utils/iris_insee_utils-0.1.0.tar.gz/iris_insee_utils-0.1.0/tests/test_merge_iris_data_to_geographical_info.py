import pandas as pd
from iris_insee_utils.merge_geographical_info_to_iris_data import (
    merge_gps_dataset_to_iris_dataset,
)


def test_merge_gps_dataset_to_iris_dataset():
    df_oi = pd.DataFrame(
        {
            "Lieu": ["Mairie de Marseille", "Site-Mémorial du Camp des Milles"],
            "longitude": [5.369905252590892, 5.382786610618382],
            "latitude": [43.296630332564405, 43.5034655315141],
        }
    )

    df_enrich = pd.DataFrame(
        {"CODE_IRIS": ["132020301", "130010905"], "Some_IRIS_Data": [100, 200]}
    )

    result = merge_gps_dataset_to_iris_dataset(
        df_oi, df_enrich, 2018, False, ("longitude", "latitude"), "CODE_IRIS"
    )

    assert isinstance(result, pd.DataFrame)
    assert "Some_IRIS_Data" in result.columns
    assert len(result) == len(df_oi)


if __name__ == "__main__":
    test_merge_gps_dataset_to_iris_dataset()
