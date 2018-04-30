# How to install
To install you must have installed python (2 or 3), have an **earthdata** acount with the applications **LP DAAC Data Pool** and **NSIDC_DATAPOOL_OPS** approved ([https://urs.earthdata.nasa.gov/](https://urs.earthdata.nasa.gov/)) and have pip installed on your computer.

# Creating a **downloader** object
To download files you have to create a downloader object. this object is created by the function `modisSuite.downloader`

```python
import modisSuite
downloaderObj = modisSuite.downloader
```
