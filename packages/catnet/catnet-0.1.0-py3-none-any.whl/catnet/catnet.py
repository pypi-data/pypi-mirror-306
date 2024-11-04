#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Creates networks of categories from literature review and other tables

Author: 
    Juan Camilo Betancur Jaramillo <juan.betancur@sei.org> - sept-2024

License:
    GNU GENERAL PUBLIC LICENSE v3 -- GNU GPLv3
"""
#                       /\_/\       *---*       *---*
#                      = o.o =     ( cat ) --> ( net )
#                      >  ^  <      *---*       *---*
#                    /--------------------------------\
#                   |     From tables to networks!     |
#                    \--------------------------------/


import pandas as pd
from pandas import DataFrame
from itertools import combinations
from importlib import resources
from pathlib import Path
from dataclasses import dataclass, field


class EdgeList(DataFrame):
    """A class for representing edges. 

    Attributes:
        DataFrame: A pd.DataFrame with at least "id", "source" and "target"
        columns.

    Methods:
        with_weights(ordered: str | None):
            Calculates the weight of each edge, aggregating the number of
            occurrences. Creates a new column "weight"
    """
    # Generates an edgelist with weights.

    def with_weights(self, ordered: str | None = None):
        """Calculates the weight of each edge, aggregating the number of
        occurrences. Creates a new column "weight"

        Args:
            ordered (str | None, optional): Should the edges be ordered in 
            ascending or descending order?. Ordered can be equal to "ascending",
            "descending" or None. Defaults to None.

        Raises:
            ValueError: if "ordered" is not equal to "ascending", "descending"
            or None.
            TypeError: if "ordered" is not type str or None

        Returns:
            _type_: _description_
        """
        # Summarise the connections in the network dataframe
        edges_with_weights = self.copy(deep=True)

        edges_with_weights.insert(
            3, "weight", [1 for i in range(len(self))])

        edges_with_weights = edges_with_weights \
            .groupby(["source", "target"]) \
            .count() \
            .reset_index() \
            .loc[:, ["source", "target", "weight"]]

        if ordered is None:
            return edges_with_weights
        elif ordered == "ascending":
            return edges_with_weights.sort_values(by="weight", ascending=True)
        elif ordered == "descending":
            return edges_with_weights.sort_values(by="weight", ascending=False)
        else:
            if type(ordered) is str or type(ordered) is None:
                raise ValueError(
                    "\"ordered\" should be either \"ascending\" or "
                    "\"descending\" ")
            else:
                raise TypeError("\"ordered\" should be type None or str ")


class NodeList(DataFrame):
    ...


@dataclass
class Network:
    """A class for representing Networks

    Attributes:
        edgelist: list of edges. It must contain at least "id", "source" and 
        "target" columns
        nodelist (optional): list of nodes. It must contain at least "id" and 
        "label" columns

    Methods:
        to_gephi(name: str, path: str, with_weights: bool):
            Exports Network to .csv files ready to be imported into a Gephi 
            project
        get_edges():
            Retrieves the edges of the Network object
        add_node_attributes(attributes: dict | DataFrame,
                            with_id: bool):
            Add new attributes to the Network.nodelist. If the new attributes 
            are provided without an "id" column, they will be added in the same 
            order to Network.nodelist.
    """
    edgelist: EdgeList
    nodelist: NodeList = field(init=False)

    def __post_init__(self):
        if self.nodelist is None:
            self.nodelist = get_nodes(self.edgelist)

    def __repr__(self) -> str:
        return "Network(" \
            f"nodelist cols: {list(self.nodelist.columns)}\n" \
            f"\tedgelist cols: {list(self.edgelist.columns)}\n" \
            ")"

    def to_gephi(self,
                 name: str,
                 path: str | None = None,
                 with_weights: bool = True) -> None:
        """Create a folder containing the .csv files with the formatting that is
        necessary to import into a Gephi project.

        Args:
            name (str): name of the folder and files to create.
            path (str | None, optional): path of the directory to create the 
            folder into. If none, it creates the folder in the current working
            directory. Defaults to None.
            with_weights (bool, optional): should the EdgeList contain weights?.
            Defaults to True.

        Raises:
            TypeError: "name" must be of str type
            TypeError: "path" must be of str type or None
            ValueError: "with_weights" must be either True or False
        """
        gephi_folder = f"{name}_gephi"
        if not isinstance(name, str):
            raise TypeError(
                f"'name' must be type string, {type(name)} was used"
            )

        if path is None:
            path = Path(gephi_folder)
            filepath = f"{name}_gephi/" + name

            if not path.exists():
                path.mkdir()
                print(f"Created directory {path.resolve()}")
                print("")

            filepath = path / name
            filepath = str(filepath).replace("\\", "/")

        elif isinstance(path, str):
            path = Path(path)
            if not path.exists():
                path.mkdir()
                print(f"Created directory {path.resolve()}")
                print("")

            filepath = path / name
            filepath = str(filepath).replace("\\", "/")
        elif not isinstance(path, (str, None)):
            raise TypeError(
                f"'path' must be either None or str, {type(path)} was"
                "used\n"
            )

        self.nodelist.to_csv(filepath + "_nodelist.csv", index=False)

        if with_weights is True:
            self.edgelist.with_weights().to_csv(filepath + "_edgelist.csv",
                                                index=False)
        elif with_weights is False:
            self.edgelist.to_csv(filepath + "_edgelist.csv", index=False)
        else:
            raise ValueError(
                f"'with_weights' must be either True or False, {with_weights}"
                " was used")

    # Returns a DataFrame with the list of edges, with or without their id
    # column
    def get_edges(self, with_id: bool = False) -> EdgeList:
        """Returns an edgelist containing only "source" and "target" columns

        Args:
            with_id (bool, optional): Should the edgelist contain the id_col?. 
            Defaults to False.

        Returns:
            EdgeList: Returns EdgeList containing the edges without attributes
        """
        if with_id:
            return (self.edgelist)
        else:
            return (self.edgelist[["source", "target"]])

    def add_node_attributes(self,
                            attributes: dict | DataFrame,
                            with_id: bool = False) -> None:
        """Add new attributes to the Network.nodelist. If the new attributes 
        are provided without an id column, they will be added in the same order
        to Network.nodelist. 

        Args:
            attributes (dict | DataFrame): must have the same length of 
                Network.nodelist
            with_id (bool, optional): True if the attributes provided contain
                an "id" column. Defaults to False.

        Raises:
            TypeError: if attributes are not a dict or a pandas DataFrame
            ValueError: if len(attributes) != len(Network.nodelist())
            TypeError: if with_id is not True of False
        """
        if isinstance(attributes, dict):
            attributes = DataFrame(attributes)
        elif isinstance(attributes, DataFrame):
            pass
        else:
            raise TypeError(
                "\"attributes\" must be either type dict or DataFrame"
            )

        if len(attributes) == len(self.nodelist):
            pass
        else:
            raise ValueError(
                "\"attributes\" must have the same length as Network.nodelist"
            )

        if with_id is False:
            updated_nodelist = pd.concat([self.nodelist, attributes], axis=1)
            self.nodelist = updated_nodelist
        elif with_id is True:
            updated_nodelist = pd.concat([self.nodelist.set_index("id"),
                                          attributes.set_index("id")],
                                         axis=1,
                                         join="inner").reset_index()
            self.nodelist = updated_nodelist
        else:
            raise TypeError(
                "\"with_id\" must be either True or False"
            )


def from_long_df(df: DataFrame,
                 id_col: str,
                 var_col: str,
                 *,
                 attr_cols: list[str] | str | None = None) -> Network:
    """Returns a network object representing the undirected connections between
    the items in a column table. It identifies the co-occurrence of items or
    categories inside the same id_col item. For example, the co-occurrence of
    categories inside the same document or publication. 

    Args:
        df (pandas.DataFrame): a long DataFrame. For the description of a "long"
        DataFrame, please refer to README
        id_col (str): the name of the column which contains the document 
        identifier
        var_col (str): the name of the column which contains the variable that
        you want to create the network.
        attr_cols (str | list[str]): list of columns that contain attributes 
        that are to be preserved in the network
, 
    Returns:
        Network: a Network object from the catnet package
    """

    # Select the required columns and drop duplicates
    df: DataFrame = df[[id_col, var_col]].drop_duplicates()

    # Create a dictionary that will contain a list of values for each id
    unpacking_dict: dict = {}
    for id in df[id_col].unique():
        unpacking_dict[id] = list(
            df[df[id_col] == id][var_col]
        )

   # Transform the dictionary into a df. Each row will have a distinct id and a
   # list of the values to create the coexistence network
    df: DataFrame = DataFrame(
        {"id":       [i[0] for i in unpacking_dict.items()],
         "items":    [i[1] for i in unpacking_dict.items()]}
    )

    # Create the source-target pairs using combinatorics
    source: list = []
    target: list = []
    id: list = []
    for i in range(len(df.id)):
        if len(df["items"][i]) > 1:
            for comb in combinations(df["items"][i], 2):
                source.append(comb[0])
                target.append(comb[1])
                id.append(df.id[i])

    # Create the network dataframe
    edges: EdgeList = EdgeList(pd.DataFrame({"id": id,
                                             "source": source,
                                             "target": target}))

    return Network(edges)


def from_same_cell(df: DataFrame,
                   id_col: str,
                   var_col: str,
                   sep: str = "\r\n",
                   *,
                   attr_cols: list[str] | str | None = None) -> Network:
    """Returns a network object representing the undirected connections between
    the items in a column table. It identifies the co-occurrence of items or
    categories inside the same id_col item. For example, the co-occurrence of
    categories inside the same document or publication. 

    Args:
        df (pandas.DataFrame): a long DataFrame. For the description of a "long"
        DataFrame, please refer to README
        id_col (str): the name of the column which contains the document 
        identifier
        var_col (str): the name of the column which contains the variable that
        you want to create the network.
        sep (str): list separator for the categories inside cell
        attr_cols (str | list[str]): list of columns that contain attributes 
        that are to be preserved in the network
, 
    Returns:
        Network: a Network object from the catnet package
    """
    if sep == "\r\n":
        df[var_col] = df[var_col].str.split("\r\n")
    elif sep == "- ":
        df[var_col] = df[var_col].str.replace("\r\n", "")
        df[var_col] = df[var_col].str.split("- ").str[1:]
    elif sep == ";":
        df[var_col] = df[var_col].str.replace("; ", ";")
        df[var_col] = df[var_col].str.split(";")
    else:
        raise ValueError("'sep' should be either '\\r\\n', ';' or '- '")

    df: DataFrame = df.explode(var_col)

    net: Network = from_long_df(df,
                                id_col=id_col,
                                var_col=var_col,
                                attr_cols=attr_cols)

    return net


def get_nodes(edgelist: EdgeList) -> NodeList:
    """Returns a DataFrame with the list of nodes. Takes an EdgeList and returns
    a NodeList object. Columns of the nodelist: "id" & "label". The nodelist can 
    contain other attributes (columns) such as color, custom size of the nodes,
    group, category, etc.

    Args:
        edges (EdgeList): must contain, at least, "source" and "target" 
        columns. 

    Returns:
        NodeList: returns a NodeList object.
    """

    return NodeList(DataFrame({
        "id":    list(set(edgelist.source) | set(edgelist.target)),
        "label": list(set(edgelist.source) | set(edgelist.target))
    }).sort_values("id").reset_index(drop=True))


# Loads the test data for exploring the package functionality
# with datasets ready to work with it
def test_data(dataset: str = "long") -> DataFrame:
    """Import test datasets

    Args:
        dataset (str, optional): Name of the dataset to be imported. It can be
        "same_cell" or "long". Defaults to "long".

    Returns:
        DataFrame: Test dataframe simulating a literature review table.
    """
    with resources.as_file(
        resources.files("catnet").joinpath("data").joinpath(f"{dataset}.csv")
    ) as f:
        data_file_path = f

    return pd.read_csv(data_file_path)
