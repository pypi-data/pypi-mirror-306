import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, PowerTransformer

class DataNormalizer:
    """
    A class used to normalize and transform numeric data in a DataFrame.

    Attributes
    ----------
    dataframe : pd.DataFrame
        The DataFrame containing numeric data to be normalized and transformed.
    """

    def __init__(self, dataframe):
        """
        Initialize the DataNormalizer with the provided DataFrame.

        Parameters
        ----------
        dataframe : pd.DataFrame
            The DataFrame to be normalized and transformed.

        Raises
        ------
        ValueError
            If the input is not a DataFrame or contains no numeric columns.
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame.")
        
        # Select only numeric columns to ensure we handle valid data for normalization and transformation
        self.dataframe = dataframe.select_dtypes(include=['number'])  
        
        # If the DataFrame doesn't contain any numeric columns, raise an error
        if self.dataframe.empty:
            raise ValueError("DataFrame contains no numeric columns.")
        
    def normalize(self, method='minmax'):
        """
        Normalize the numeric data in the DataFrame using the specified method.

        Parameters
        ----------
        method : str, optional
            The normalization method to use ('minmax', 'zscore', 'robust'). 
            Default is 'minmax'.
            - 'minmax' scales data to a range [0, 1].
            - 'zscore' (StandardScaler) standardizes data to have zero mean and unit variance.
            - 'robust' (RobustScaler) is less sensitive to outliers and scales data based on interquartile range.

        Returns
        -------
        pd.DataFrame
            A DataFrame with normalized numeric values based on the chosen method.

        Raises
        ------
        ValueError
            If an unsupported normalization method is provided.
        """
        # Define available normalization methods and their corresponding scalers
        methods = {
            'minmax': MinMaxScaler,
            'zscore': StandardScaler,
            'robust': RobustScaler
        }
        
        # Raise error if the provided method is not supported
        if method not in methods:
            raise ValueError(f"Unsupported normalization method '{method}'. Supported methods are: {', '.join(methods.keys())}.")
        
        # Initialize the chosen scaler and apply it to the numeric columns of the DataFrame
        scaler = methods[method]()
        normalized_df = pd.DataFrame(scaler.fit_transform(self.dataframe), columns=self.dataframe.columns)
        
        # Return the normalized DataFrame
        return normalized_df

    def transform(self, method='log'):
        """
        Transform the numeric data in the DataFrame using the specified transformation method.

        Parameters
        ----------
        method : str, optional
            The transformation method to use ('log', 'sqrt', 'boxcox'). 
            Default is 'log'.
            - 'log' applies a log transformation to reduce skewness.
            - 'sqrt' applies a square root transformation, often used for count data.
            - 'boxcox' applies a Box-Cox transformation, which is commonly used for stabilizing variance and normalizing data.

        Returns
        -------
        pd.DataFrame
            A DataFrame with transformed numeric values based on the chosen method.

        Raises
        ------
        ValueError
            If an unsupported transformation method is provided.
        """
        # Create a copy of the numeric DataFrame to avoid modifying the original data
        transformed_df = self.dataframe.copy()

        # Apply the chosen transformation method
        if method == 'log':
            # Log transformation using log1p (log(1+x)) to handle zero values
            transformed_df = np.log1p(self.dataframe)
        elif method == 'sqrt':
            # Square root transformation
            transformed_df = np.sqrt(self.dataframe)
        elif method == 'boxcox':
            # Box-Cox transformation, which only works for strictly positive data
            pt = PowerTransformer(method='box-cox', standardize=False)
            transformed_df = pd.DataFrame(pt.fit_transform(self.dataframe), columns=self.dataframe.columns)
        else:
            # Raise error if the provided transformation method is not supported
            raise ValueError(f"Unsupported transformation method '{method}'. Supported methods are: log, sqrt, boxcox.")
        
        # Return the transformed DataFrame
        return transformed_df

    @staticmethod
    def log_message(message):
        """
        Log a message to the console.

        Parameters
        ----------
        message : str
            The message to log.
        """
        print(f"Error: {message}")

