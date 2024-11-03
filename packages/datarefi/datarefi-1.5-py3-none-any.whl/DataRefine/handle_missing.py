import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer  # Enables IterativeImputer
from sklearn.impute import IterativeImputer
import plotly.graph_objects as go

class MissingDataHandler:
    """
    A class to handle missing data detection, imputation, and visualization.

    Attributes:
    ----------
    dataframe : pd.DataFrame
        The input DataFrame on which missing data operations will be performed.

    Methods:
    -------
    detect_missing_values(dataframe=None):
        Detects and returns the count of missing values in each column of the DataFrame.

    impute_missing(strategy='mean', fill_value=None, dataframe=None, **kwargs):
        Imputes missing values in the DataFrame using different strategies.

    plot_missing_values(dataframe=None):
        Plots a bar chart showing the count of missing values in each column using Plotly.

    log_message(message):
        Logs an error message to the console.
    """

    def __init__(self, dataframe):
        """
        Initializes the MissingDataHandler with a pandas DataFrame.

        Parameters:
        ----------
        dataframe : pd.DataFrame
            The DataFrame to perform missing data operations on.
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("The input must be a pandas DataFrame.")
        self.dataframe = dataframe

    def detect_missing_values(self, dataframe=None):
        """
        Detects missing values in the DataFrame and returns the count per column.

        Parameters:
        ----------
        dataframe : pd.DataFrame, optional
            The DataFrame to check for missing values. If not provided, the original DataFrame is used.

        Returns:
        -------
        pd.Series
            A series containing the count of missing values per column.
        """
        if dataframe is None:
            dataframe = self.dataframe
        missing_data_count = dataframe.isnull().sum()
        return missing_data_count

    def impute_missing(self, strategy='mean', fill_value=None, dataframe=None, **kwargs):
        """
        Imputes missing values in the DataFrame using different strategies.

        Parameters:
        ----------
        strategy : str, optional
            The imputation strategy. Options are 'mean', 'median', 'most_frequent', 'predictive', and 'custom'.
            Default is 'mean'.
        fill_value : any, optional
            The value to fill missing data when strategy='custom'.
        dataframe : pd.DataFrame, optional
            The DataFrame to impute. If not provided, the original DataFrame is used.
        **kwargs : optional
            Additional keyword arguments for the IterativeImputer when strategy='predictive'.

        Returns:
        -------
        pd.DataFrame
            The DataFrame with missing values imputed.

        Raises:
        ------
        ValueError
            If an unsupported strategy is provided or if required parameters are missing.
        """
        try:
            if dataframe is None:
                dataframe = self.dataframe
            
            # Replace None with np.nan for consistency
            dataframe = dataframe.replace({None: np.nan})
            
            # Detect missing values before imputation (optional)
            missing_data_before = self.detect_missing_values(dataframe)
            
            # Choose imputation strategy
            if strategy in ['mean', 'median', 'most_frequent']:
                imputer = SimpleImputer(strategy=strategy)
            elif strategy == 'predictive':
                imputer = IterativeImputer(**kwargs)
            elif strategy == 'custom':
                if fill_value is None:
                    raise ValueError("fill_value must be provided for custom imputation")
                imputer = SimpleImputer(strategy='constant', fill_value=fill_value)
            else:
                raise ValueError("Unsupported imputation strategy")
            
            # Perform imputation
            imputed_data = imputer.fit_transform(dataframe)
            dataframe = pd.DataFrame(imputed_data, columns=dataframe.columns)
            return dataframe
        
        except ValueError as e:
            self.log_message(str(e))
            raise
        except Exception as e:
            self.log_message(f"An unexpected error occurred: {str(e)}")
            raise

    def plot_missing_values(self, dataframe=None):
        """
        Plots a bar chart showing the count of missing values in each column using Plotly.

        Parameters:
        ----------
        dataframe : pd.DataFrame, optional
            The DataFrame to plot missing values for. If not provided, the original DataFrame is used.

        Returns:
        -------
        plotly.graph_objs.Figure
            A Plotly figure object with the bar chart of missing values.
        """
        if dataframe is None:
            dataframe = self.dataframe
        missing_data_count = self.detect_missing_values(dataframe)
        
        # Create Plotly bar chart for missing values
        fig = go.Figure(go.Bar(
            x=missing_data_count.index,
            y=missing_data_count.values,
            text=missing_data_count.values,
            textposition='auto',
        ))
        fig.update_layout(
            title="Count of Missing Values by Column",
            xaxis_title="Columns",
            yaxis_title="Count of Missing Values",
            template="plotly_white"
        )
        return fig  # Return the Plotly Figure object

    @staticmethod
    def log_message(message):
        """
        Logs an error message to the console.

        Parameters:
        ----------
        message : str
            The error message to log.
        """
        print(f"Error: {message}")
