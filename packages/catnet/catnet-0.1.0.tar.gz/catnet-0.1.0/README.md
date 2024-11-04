# catnet
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14031788.svg)](https://doi.org/10.5281/zenodo.14031788)

## What catnet does
`catnet` is a Python package that allows for transforming tabular data into a network structure. `catnet` can identify the coexistence of variables and categories in literature reviews and other tables and create a network dataframe that can be exported into a format that can be taken by other packages such as `networkx` and applications such as [Gephi](https://gephi.org/).

`catnet` is a Python package designed to facilitate the creation and analysis of category networks. Whether you’re working with literature review tables or other structured data, `catnet` empowers researchers and analysts to build insightful networks that reveal relationships and patterns within their categories. Streamline your data exploration and enhance your analytical capabilities with catnet!

## How to install catnet
To install this package run:

`python -m pip install git+https://github.com/CamiBetancur/catnet/)`

## Get started using catnet

To be able to use `catnet` you need to format your dataframe in one of the following ways:

### 1. **"Long" format**
"Long" format refers to data that has a column for describing a categorical variable (`var_col`) and an identifier column (`id_col`) that identifies to which entity that variable belongs to. For example, in a literature review, a long dataframe that could be used by catnet could look like this (note that the column names `id_col` and `var_col` do not necessarily need to be named `id_col` and `var_col`):

| id_col | var_col            | other_data_cols |
| ------ | ------------------ | --------------- |
| doc_01 | Health             | ...             |
| doc_01 | Water access       | ...             |
| doc_01 | Water quality      | ...             |
| doc_02 | Health             | ...             |
| doc_02 | Energy generation  | ...             |
|  ...   |   ...              | ...             |

Datasets in "long" format can be transformed into networks by using the `catnet.from_long_df()` function. For more information, you can look at the [Examples Jupyter Notebook](https://github.com/CamiBetancur/catnet/blob/main/Examples.ipynb) or the [Examples Markdown file](https://github.com/CamiBetancur/catnet/blob/main/Examples.md).

### 2. **"Same cell" format**
Dataframes in the "same cell" format contain a list of categories insid the same cell. The identifier colum (`id_col`) marks different documents/observations, while the categorical variable column (`var_col`) contains the lists of categories.

| id_col | var_col            | other_data_cols |
| ------ | ------------------ | --------------- |
| doc_01 | Health; Water      | ...             |
|        | access; Water      |                 |
|        | quality            |                 |
| doc_02 | Health; Energy     | ...             |
|        | generation         |                 |
|  ...   |   ...              | ...             |

Datasets in the "same cell" format can be transformed into networks by using the `catnet.from_same_cell()` function. For more information, you can look at the [Examples Jupyter Notebook](https://github.com/CamiBetancur/catnet/blob/main/Examples.ipynb) or the [Examples Markdown file](https://github.com/CamiBetancur/catnet/blob/main/Examples.md).

## How to cite catnet

### APA 7

>Betancur Jaramillo, J. C. (2024). _catnet source code (Version 0.1.0)_ [source code]. [https://github.com/CamiBetancur/catnet/](https://github.com/CamiBetancur/catnet/). 

### BibTex

```
@misc{Betancur_2024,  
      title={catnet v0.1.0},  
      url={https://github.com/CamiBetancur/catnet},  
      publisher={Stockholm Environment Institute},  
      author={Betancur Jaramillo, Juan Camilo},  
      year={2024}}  
```