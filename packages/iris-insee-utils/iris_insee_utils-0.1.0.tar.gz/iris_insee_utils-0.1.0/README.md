[![codecov](https://codecov.io/gh/adrienpacifico/iris_insee_utils/branch/master/graph/badge.svg?token=ZZItjohsp9)](https://codecov.io/gh/adrienpacifico/iris_insee_utils)  
Note: This repository library is currently under construction and is not now usable as is.


This repository aims to provide an easy solution to determine to which iris GPS coordinates correspond.
This could be extended to a transformation from address to iris.


### Usage:

 ```python
>>>from iris_insee_util import gps_to_iris

>>>gps_to_iris(lat, long, iris_year=2018)
132030402

 ```



More information about IRIS:
https://www.insee.fr/fr/information/5008701?sommaire=5008710#titre-bloc-32

Related project: 
https://github.com/Oslandia/pyris