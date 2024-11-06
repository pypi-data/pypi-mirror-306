import folium
import unittest
from iris_insee_utils.iris_map import plot_folium_map
import pandas as pd
import os


class TestFoliumMap(unittest.TestCase):

    def test_plot_folium_map(self):
        # Call the function to generate the map
        m = plot_folium_map(commune_name="Nice", iris_year=2018)

        # Check if the returned object is a Folium Map
        self.assertIsInstance(m, folium.Map)

        # Generate HTML content
        html_content = m.get_root().render()

        print(html_content[:2000])
        # Check if the HTML content contains expected elements
        self.assertIn('<div class="folium-map"', html_content)
        self.assertIn("Nice", html_content)  # Check if the commune name is in the HTML

    def test_plot_folium_map_with_df_oi(self):
        df_oi = pd.DataFrame(
            {
                "Lieu": ["Mairie de Marseille", "Site-Mémorial du Camp des Milles"],
                "lon": [5.369905252590892, 5.382786610618382],
                "lat": [43.296630332564405, 43.5034655315141],
            }
        )

        m = plot_folium_map(iris_year=2018, commune_name="Marseille", df_oi=df_oi)
        self.assertIsInstance(m, folium.Map)

    def test_plot_folium_map_df_enrich(self):
        df_oi = pd.DataFrame(
            {
                "Lieu": ["Mairie de Marseille", "Site-Mémorial du Camp des Milles"],
                "lon": [5.369905252590892, 5.382786610618382],
                "lat": [43.296630332564405, 43.5034655315141],
            }
        )

        df_enrich = pd.DataFrame(
            {"CODE_IRIS": ["132020301", "130010905"], "Some_IRIS_Data": [100, 200]}
        )

        save_map_path = "test_map.html"

        m = plot_folium_map(
            iris_year=2018,
            commune_name="Marseille",
            df_oi=df_oi,
            df_enrich=df_enrich,
            df_enrich_iriscol_colname="CODE_IRIS",
            df_enrich_select_cols=["Some_IRIS_Data"],
        )

        assert isinstance(m, folium.Map)


def test_plot_folium_map():
    save_map_path = "test_map.html"
    m = plot_folium_map(
        commune_name="Nice", iris_year=2018, save_map_path=save_map_path
    )

    assert isinstance(m, folium.Map)
    assert os.path.exists(save_map_path)

    # Clean up
    os.remove(save_map_path)


if __name__ == "__main__":
    unittest.main()
