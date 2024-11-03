import pandas as pd

class DataQualityAssessment:
    """
    A class for assessing the quality of a DataFrame, including summary statistics
    and quality metrics such as missing values and outliers.

    Attributes
    ----------
    dataframe : pd.DataFrame
        The DataFrame to be assessed, containing numeric columns only.

    Methods
    -------
    summary_statistics():
        Computes and returns summary statistics for the DataFrame, including skewness and kurtosis.
    quality_metrics():
        Computes and returns quality metrics for the DataFrame, such as missing values and outliers.
    log_message(message):
        Logs error messages to the console.
    """

    def __init__(self, dataframe):
        """
        Initializes the DataQualityAssessment class with the given DataFrame.

        Parameters
        ----------
        dataframe : pd.DataFrame
            The DataFrame to be assessed, containing numeric columns only.

        Raises
        ------
        ValueError
            If the input is not a pandas DataFrame or if no numeric columns are found in the DataFrame.
        """
        # Ensure the input is a pandas DataFrame
        if not isinstance(dataframe, pd.DataFrame):
            self.log_message("The input must be a pandas DataFrame.")
            raise ValueError("The input must be a pandas DataFrame.")
        
        # Select only numeric columns
        numeric_columns = dataframe.select_dtypes(include=['number']).columns
        if len(numeric_columns) == 0:
            self.log_message("No numeric columns found in the DataFrame.")
            raise ValueError("No numeric columns found in the DataFrame.")

        # Set the dataframe attribute to only contain numeric columns
        self.dataframe = dataframe[numeric_columns]

    def summary_statistics(self):
        """
        Computes and returns summary statistics for the DataFrame, including skewness and kurtosis.

        Summary statistics include:
        - Mean, standard deviation, min, max, and quartiles (25%, 50%, 75%).
        - Skewness: Measures the asymmetry of the data distribution.
        - Kurtosis: Measures the "tailedness" of the distribution (i.e., outliers).

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the summary statistics for each numeric column.

        Raises
        ------
        Exception
            If an error occurs while computing the statistics.
        """
        try:
            # Basic descriptive statistics for numeric columns
            stats_df = self.dataframe.describe().T
            
            # Calculate skewness for each numeric column
            stats_df['skewness'] = self.dataframe.skew()
            
            # Calculate kurtosis for each numeric column
            stats_df['kurtosis'] = self.dataframe.kurtosis()

            return stats_df
        
        except Exception as e:
            # Log the error message and return an empty DataFrame
            self.log_message(f"Error computing summary statistics: {str(e)}")
            return pd.DataFrame()

    def quality_metrics(self):
        """
        Computes and returns quality metrics for the DataFrame, such as missing values and outliers.

        Quality metrics include:
        - Missing values: Count of missing values in each numeric column.
        - Outliers: Count of outliers, defined as values above the 99th percentile.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the missing values and outlier counts for each numeric column.

        Raises
        ------
        Exception
            If an error occurs while computing the quality metrics.
        """
        try:
            # Calculate the number of missing values for each numeric column
            missing_values = self.dataframe.isnull().sum()
            
            # Calculate the number of outliers (values greater than the 99th percentile)
            outliers = (self.dataframe > self.dataframe.quantile(0.99)).sum()
            
            # Combine missing values and outliers into a DataFrame
            data_quality = pd.DataFrame({
                'missing_values': missing_values,
                'outliers': outliers
            })

            return data_quality
        
        except Exception as e:
            # Log the error message and return an empty DataFrame
            self.log_message(f"Error computing quality metrics: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def log_message(message):
        """
        Logs a message to the console.

        Parameters
        ----------
        message : str
            The message to log.
        """
        print(f"Error: {message}")
