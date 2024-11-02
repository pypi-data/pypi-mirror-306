from typing import List

import polars as pl


class DataFrameDataSource:
    """
    polars DataFrame DataSource to manage data retrieval from DataFrames.

    Attributes:
        dataframe (pl.DataFrame): DataFrame containing the data.
    """

    def __init__(self, dataframe: pl.DataFrame):
        self.dataframe = dataframe

    @property
    def dataframe(self) -> pl.DataFrame:
        """
        Get the DataFrame containing the data.

        Returns:
            pl.DataFrame: DataFrame containing the data.
        """
        return self.__dataframe

    @dataframe.setter
    def dataframe(self, dataframe: pl.DataFrame) -> None:
        """
        Set the DataFrame containing the data.

        Args:
            dataframe (pl.DataFrame): DataFrame containing the data.

        Raises:
            TypeError: If 'dataframe' is not a polars DataFrame.
        """
        if not isinstance(dataframe, pl.DataFrame):
            raise TypeError("'dataframe' must be a polars DataFrame.")
        self.__dataframe = dataframe

    def fetch_data(self) -> pl.DataFrame:
        """
        Fetch data from the DataFrame.

        Returns:
            pl.DataFrame: DataFrame containing the data.
        """
        if self.dataframe is None:
            raise RuntimeError("No data loaded in the DataFrame.")
        return self.dataframe

    def get_columns(self) -> List[str]:
        """
        Get the list of column names from the DataFrame.

        Returns:
            List[str]: Column names.
        """
        if self.dataframe is None:
            raise RuntimeError("No data loaded in the DataFrame.")
        return list(self.dataframe.columns)

    def filter_data(self, query: str) -> pl.DataFrame:
        """
        Filter the data in the DataFrame using a query.

        Args:
            query (str): Query to filter the data.

        Returns:
            pl.DataFrame: Filtered DataFrame.

        Raises:
            RuntimeError: If no data is loaded in the DataFrame.
            ValueError: If no query is provided.
            ValueError: If query is an empty string.
            TypeError: If query is not a string.
        """
        if self.dataframe is None:
            raise RuntimeError("No data loaded in the DataFrame.")
        if not query:
            raise ValueError("Query must be provided to filter the data.")
        if not isinstance(query, str):
            raise TypeError("'query' must be a string.")
        if query.strip() == "":
            raise ValueError("Query cannot be an empty string.")

        return self.dataframe.sql(query)

    def __str__(self) -> str:
        """
        Get the string representation of the DataFrameDataSource.

        Returns:
            str: String representation of the DataFrameDataSource.
        """
        return (
            f"DataFrameDataSource(dataframe with {self.dataframe.shape[0]} rows"
            f" and {self.dataframe.shape[1]} columns)"
        )
