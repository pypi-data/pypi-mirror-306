[![codecov](https://codecov.io/gh/adrienpacifico/iris_insee_utils/branch/master/graph/badge.svg?token=ZZItjohsp9)](https://codecov.io/gh/adrienpacifico/iris_insee_utils)  
Note: This library is currently in beta and may contain bugs. Please use it with caution.

This repository provides an easy solution to determine which IRIS zone (Ilots Regroupés pour l'Information Statistique) corresponds to a set of GPS coordinates. It also includes utilities to plot maps with IRIS contours, enrich IRIS-specific data, and manage external data containing GPS points.

### Install
`pip install iris_insee_utils`

### Usage:

 ```python
>>>from iris_insee_utils import gps_to_code_iris

>>>gps_to_iris(lat, long, iris_year=2018)
'920200101'
 ```

Working with a dataframe with longitude and latitude:

```python
>>> df_gps_to_iris(df, long_col, lat_col, iris_year=2020)
                               Lieu longitude latitude  IRIS  CODE_IRIS            NOM_IRIS
0               Mairie de Marseille     5.369   43.296  0301  132020301        Quai du Port
1  Site-Mémorial du Camp des Milles     5.382   43.503  0905  130010905  Les Milles Village
```

Plot a map with data that enriches the IRIS level:

```python
plot_folium_map(
    2020,
    "Paris",
    df_enrich=df_enrich,
    df_enrich_iriscol_colname="IRIS",
    df_enrich_select_cols=["Nombre de ménges","Nombre de personnes"]
)
```
![alt text](img/image.png)


```python
plot_folium_map(2018, "Limoges", df_oi=df_bus_stops)
```
![alt text](img/image-3.png)



More information about IRIS:
https://www.insee.fr/fr/information/5008701?sommaire=5008710#titre-bloc-32

Related project: 
https://github.com/Oslandia/pyris