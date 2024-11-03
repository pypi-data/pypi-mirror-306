import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io
import logging
import traceback
from DataRefine.handle_missing import MissingDataHandler
from DataRefine.handle_outliers import OutlierHandler
from DataRefine.normalize import DataNormalizer
from DataRefine.data_quality_assessment import DataQualityAssessment
import pkg_resources

logo_path = pkg_resources.resource_filename('DataRefine', 'scripts/drlogo.jpeg')
st.set_page_config(
    page_title="DataRefine",
    page_icon=logo_path,
    layout="wide"
)

# Set up logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler()]
)

def log_error(e):
    """Log the error with traceback."""
    logging.error(f"Error: {e}")
    logging.error(traceback.format_exc())

def show_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='color: #2a98bd;'>DataRefine</h1>", unsafe_allow_html=True)
        st.image("scripts/drlogo.jpeg", caption=None, width=200)

def upload_file():
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                initialize_session_state(df)
                st.markdown("<p style='color: #2a98bd;'>File uploaded successfully!</p>", unsafe_allow_html=True)
                if st.button("Go to Data Cleaning"):
                    st.session_state.page = 'analysis'
                    st.experimental_rerun()
            except pd.errors.EmptyDataError:
                st.error("The uploaded file is empty. Please upload a valid CSV file.")
            except pd.errors.ParserError:
                st.error("The uploaded file could not be parsed. Please ensure it is a valid CSV file.")
            except Exception as e:
                st.error("An unexpected error occurred while loading the file.")
                log_error(e)

def initialize_session_state(df):
    st.session_state.df = df
    update_session_state()

def update_session_state():
    df = st.session_state.df
    st.session_state.handler = MissingDataHandler(df)
    st.session_state.outlier_handler = OutlierHandler(df)
    st.session_state.normalizer = DataNormalizer(df)
    st.session_state.quality_assessor = DataQualityAssessment(df)

def show_data_overview():
    st.markdown("<h2 style='color: #2a98bd;'>Data Overview</h2>", unsafe_allow_html=True)
    df = st.session_state.df
    st.write("**Data Shape:**", df.shape)
    st.write("**DataFrame:**", df)
    st.write("**Data Information:**")
    buffer = io.StringIO()
    try:
        df.info(buf=buffer)
        buffer.seek(0)
        info_lines = buffer.getvalue().splitlines()
        data_lines = info_lines[5:-2]
        if data_lines:
            table_data = []
            for line in data_lines:
                parts = line.split()
                if len(parts) >= 3:
                    column = ' '.join(parts[:-2])
                    non_null_count = parts[-2] + ' ' + parts[-1]
                    dtype = parts[-3]
                    column = ' '.join(part.lstrip('0123456789') for part in column.split())
                    table_data.append([column, non_null_count, dtype])
            table_df = pd.DataFrame(table_data, columns=["Column", "Dtype", "Non-Null Count"])
            st.write(table_df)
    except Exception as e:
        st.error("An error occurred while displaying data information.")
        log_error(e)

def handle_missing_values():
    st.markdown("<h2 style='color: #2a98bd;'>Missing Values Detection and Handling</h2>", unsafe_allow_html=True)
    
    # Store original DataFrame if not already stored
    if 'df_before_imputation' not in st.session_state:
        st.session_state.df_before_imputation = st.session_state.df.copy()
    
    # Create two columns for before/after comparison
    col1, col2 = st.columns(2)
    
    handler = st.session_state.handler
    
    with col1:
        st.write("**Original DataFrame with Missing Values:**")
        st.write(st.session_state.df_before_imputation)
        
        # Plot original missing values
        st.plotly_chart(handler.plot_missing_values(st.session_state.df_before_imputation))

    st.sidebar.write("### Handle Missing Values")
    columns = st.sidebar.multiselect(
        "Select Columns for Imputation",
        options=st.session_state.df_before_imputation.columns.tolist(),
        default=st.session_state.df_before_imputation.columns.tolist()
    )
    
    strategy = st.sidebar.selectbox(
        "Select Imputation Strategy",
        ["mean", "median", "most_frequent", "predictive", "custom"]
    )
    
    fill_value = None
    if strategy == "custom":
        fill_value = st.sidebar.text_input("Fill Value", value="0")

    if st.sidebar.button("Impute Missing Values"):
        with st.spinner("Imputing missing values..."):
            try:
                if not columns:
                    st.warning("No columns selected for imputation. Please select at least one column.")
                    return
                
                # Create a copy for imputation
                df_imputed = st.session_state.df_before_imputation.copy()
                
                # Perform imputation on selected columns
                df_subset = df_imputed[columns].copy()
                df_imputed_subset = handler.impute_missing(strategy, fill_value=fill_value, dataframe=df_subset)
                
                # Update only the selected columns
                df_imputed[columns] = df_imputed_subset
                
                # Store imputed DataFrame in session state
                st.session_state.df = df_imputed
                update_session_state()
                
                with col2:
                    st.write("**DataFrame After Imputation:**")
                    st.write(df_imputed)
                    
                    st.plotly_chart(handler.plot_missing_values(df_imputed))
                
                st.success("Missing values imputed successfully.")
                
            except Exception as e:
                st.error("An unexpected error occurred during imputation.")
                log_error(e)
    
    # If imputed data exists but button wasn't just clicked, still show it
    elif 'df' in st.session_state and not st.session_state.df.equals(st.session_state.df_before_imputation):
        with col2:
            st.write("**DataFrame After Imputation:**")
            st.write(st.session_state.df)
            
            st.plotly_chart(handler.plot_missing_values(st.session_state.df))

def handle_outliers():
    st.markdown("<h2 style='color: #2a98bd;'>Outlier Detection and Handling</h2>", unsafe_allow_html=True)
    
    # Store original DataFrame if not already stored
    if 'df_before_outlier_handling' not in st.session_state:
        st.session_state.df_before_outlier_handling = st.session_state.df.copy()
    
    # Create two columns for before/after comparison
    col1, col2 = st.columns(2)
    
    # Display original DataFrame first (fixed position)
    with col1:
        st.write("**Original DataFrame:**")
        st.write(st.session_state.df_before_outlier_handling)
    
    outlier_handler = st.session_state.outlier_handler
    
    # Sidebar controls with IQR as default
    st.sidebar.write("### Outlier Detection Options")
    method = st.sidebar.selectbox(
        "Select Outlier Detection Method", 
        ["iqr", "zscore"],
        index=0,
        help="IQR: Interquartile Range method\nZ-score: Standard deviation based method"
    )
    
    # Dynamic threshold suggestion based on method
    default_threshold = 1.5 if method == "iqr" else 3.0
    threshold = st.sidebar.slider(
        "Select Threshold", 
        0.0, 5.0, default_threshold, 0.1,
        help="IQR method: Typically use 1.5 (default) or 3.0\nZ-score method: Typically use 3.0"
    )
    
    try:
        # Detect outliers using the original data
        outliers_df, outlier_counts = outlier_handler.detect_outliers(
            method=method,
            threshold=threshold
        )

        
        # Get numerical columns for box plot
        numerical_columns = st.session_state.df_before_outlier_handling.select_dtypes(
            include=['number']
        ).columns.tolist()
        
        # Column selection for box plot
        selected_column = st.sidebar.selectbox(
            "Select Column to see Box Plot Distribution",
            options=numerical_columns
        )
        
        # Always show the original box plot if column is selected
        if selected_column:
            with col1:
                box_fig = go.Figure()
                box_fig.add_trace(go.Box(
                    y=st.session_state.df_before_outlier_handling[selected_column],
                    name="Original",
                    boxpoints='outliers',
                    marker_color='blue'
                ))
                box_fig.update_layout(
                    title=f'Original Distribution of {selected_column}',
                    yaxis_title=selected_column
                )
                st.plotly_chart(box_fig)
        
        # Outlier handling controls
        st.sidebar.write("### Handle Outliers")
        handling_method = st.sidebar.selectbox(
            "Select Outlier Handling Method",
            ["cap", "remove", "impute"],
            help="""
            cap: Replace outliers with threshold values
            remove: Delete rows with outliers
            impute: Replace outliers with median values
            """
        )
        
        if st.sidebar.button("Handle Outliers"):
            with st.spinner("Handling outliers..."):
                try:
                    # Handle outliers
                    df_handled, old_counts, new_counts = outlier_handler.handle_outliers(
                        method=handling_method,
                        detection_method=method,
                        threshold=threshold
                    )
                    
                    # Update session state with handled data
                    st.session_state.df = df_handled
                    update_session_state()
                    
                    # Display results in right column
                    with col2:
                        st.write("**DataFrame After Outlier Handling:**")
                        st.write(df_handled)
                        
                        # Show updated box plot if column is selected
                        if selected_column:
                            new_box_fig = go.Figure()
                            new_box_fig.add_trace(go.Box(
                                y=df_handled[selected_column],
                                name="After Handling",
                                boxpoints='outliers',
                                marker_color='green'
                            ))
                            new_box_fig.update_layout(
                                title=f'Distribution After Handling: {selected_column}',
                                yaxis_title=selected_column
                            )
                            st.plotly_chart(new_box_fig)
                    
                    st.success("Outliers handled successfully!")
                    
                except Exception as e:
                    st.error("An error occurred during outlier handling.")
                    log_error(e)
        
        # If handled data exists but button wasn't just clicked, still show it
        elif 'df' in st.session_state and not st.session_state.df.equals(st.session_state.df_before_outlier_handling):
            with col2:
                st.write("**DataFrame After Outlier Handling:**")
                st.write(st.session_state.df)
                
                # Show box plot for handled data if column is selected
                if selected_column:
                    new_box_fig = go.Figure()
                    new_box_fig.add_trace(go.Box(
                        y=st.session_state.df[selected_column],
                        name="After Handling",
                        boxpoints='outliers',
                        marker_color='green'
                    ))
                    new_box_fig.update_layout(
                        title=f'Distribution After Handling: {selected_column}',
                        yaxis_title=selected_column
                    )
                    st.plotly_chart(new_box_fig)
                    
    except Exception as e:
        st.error("An unexpected error occurred.")
        log_error(e)
        
def normalize_data():
    st.markdown("<h2 style='color: #2a98bd;'>Data Normalization</h2>", unsafe_allow_html=True)

    # Store original DataFrame if not already stored
    if 'df_before_normalization' not in st.session_state:
        st.session_state.df_before_normalization = st.session_state.df.copy()

    # Create two columns for before/after comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Original DataFrame:**")
        st.write(st.session_state.df_before_normalization)
    
    normalizer = st.session_state.normalizer

    st.sidebar.write("### Normalization Options")
    normalization_method = st.sidebar.selectbox("Select Normalization Method", ["minmax", "zscore", "robust"])
    columns_to_normalize = st.sidebar.multiselect(
        "Select Columns to Normalize",
        options=st.session_state.df_before_normalization.select_dtypes(include=['number']).columns.tolist(),
        default=st.session_state.df_before_normalization.select_dtypes(include=['number']).columns.tolist()
    )

    # Always show before plot based on original data
    selected_column = st.sidebar.selectbox(
        "Select Column to Plot", 
        options=columns_to_normalize if columns_to_normalize else []
    )

    if selected_column:
        with col1:
            fig_before = go.Figure()
            fig_before.add_trace(go.Histogram(
                x=st.session_state.df_before_normalization[selected_column], 
                nbinsx=50, 
                marker_color='lightblue',
                name='Original'
            ))
            fig_before.update_layout(
                title=f"Original Distribution: {selected_column}", 
                xaxis_title=selected_column, 
                yaxis_title='Count'
            )
            st.plotly_chart(fig_before)

    # Handle normalization when button is clicked
    if st.sidebar.button("Apply Normalization"):
        with st.spinner("Normalizing data..."):
            try:
                if st.session_state.df_before_normalization is None or st.session_state.df_before_normalization.empty:
                    st.error("The DataFrame is empty or None. Please check if data was loaded correctly.")
                    return

                if not columns_to_normalize:
                    st.warning("No columns selected for normalization. Please select at least one column.")
                    return

                # Create a copy for normalization
                normalized_df = st.session_state.df_before_normalization.copy()
                
                # Only keep selected columns for normalization
                temp_df = normalized_df[columns_to_normalize].copy()
                
                # Create a new normalizer with only selected columns
                temp_normalizer = DataNormalizer(temp_df)
                
                # Apply normalization
                normalized_columns = temp_normalizer.normalize(method=normalization_method)
                
                # Update only the selected columns in the full DataFrame
                for col in columns_to_normalize:
                    normalized_df[col] = normalized_columns[col]

                # Store normalized DataFrame in session state
                st.session_state.df = normalized_df
                update_session_state()

                with col2:
                    st.write("**Normalized DataFrame:**")
                    st.write(normalized_df)

                    if selected_column:
                        fig_after = go.Figure()
                        fig_after.add_trace(go.Histogram(
                            x=normalized_df[selected_column], 
                            nbinsx=50, 
                            marker_color='lightgreen',
                            name='Normalized'
                        ))
                        fig_after.update_layout(
                            title=f"Normalized Distribution: {selected_column}", 
                            xaxis_title=selected_column, 
                            yaxis_title='Count'
                        )
                        st.plotly_chart(fig_after)

                st.success("Data normalized successfully.")

            except Exception as e:
                st.error(f"An unexpected error occurred during normalization: {str(e)}")
                log_error(e)
    
    # If normalized data exists but button wasn't just clicked, still show it
    elif 'df' in st.session_state and not st.session_state.df.equals(st.session_state.df_before_normalization):
        with col2:
            st.write("**Normalized DataFrame:**")
            st.write(st.session_state.df)

            if selected_column:
                fig_after = go.Figure()
                fig_after.add_trace(go.Histogram(
                    x=st.session_state.df[selected_column], 
                    nbinsx=50, 
                    marker_color='lightgreen',
                    name='Normalized'
                ))
                fig_after.update_layout(
                    title=f"Normalized Distribution: {selected_column}", 
                    xaxis_title=selected_column, 
                    yaxis_title='Count'
                )
                st.plotly_chart(fig_after)


def transform_data():
    st.markdown("<h2 style='color: #2a98bd;'>Data Transformation</h2>", unsafe_allow_html=True)
    
    # Store original DataFrame if not already stored
    if 'df_before_transformation' not in st.session_state:
        st.session_state.df_before_transformation = st.session_state.df.copy()
    
    # Create two columns for before/after comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Original DataFrame:**")
        st.write(st.session_state.df_before_transformation)
    
    st.sidebar.write("### Transformation Options")
    
    # Initialize DataNormalizer
    try:
        normalizer = DataNormalizer(st.session_state.df_before_transformation)
    except ValueError as e:
        st.error(str(e))
        return
    
    # Use methods available in DataNormalizer
    transformation_method = st.sidebar.selectbox(
        "Select Transformation Method",
        ["log", "sqrt", "boxcox"]  # Methods available in DataNormalizer.transform()
    )
    
    columns_to_transform = st.sidebar.multiselect(
        "Select Columns to Transform",
        options=normalizer.dataframe.columns.tolist(),
        default=normalizer.dataframe.columns.tolist()
    )
    
    # Always show before plot based on original data
    selected_column = st.sidebar.selectbox(
        "Select Column to Plot",
        options=columns_to_transform if columns_to_transform else []
    )

    if selected_column:
        with col1:
            fig_before = go.Figure()
            fig_before.add_trace(go.Histogram(
                x=st.session_state.df_before_transformation[selected_column],
                nbinsx=50,
                marker_color='lightblue',
                name='Original'
            ))
            fig_before.update_layout(
                title=f"Original Distribution: {selected_column}",
                xaxis_title=selected_column,
                yaxis_title='Count'
            )
            st.plotly_chart(fig_before)

    # Handle transformation when button is clicked
    if st.sidebar.button("Apply Transformation"):
        with st.spinner("Transforming data..."):
            try:
                if not columns_to_transform:
                    st.warning("No columns selected for transformation. Please select at least one column.")
                    return

                # Create a copy for transformation
                transformed_df = st.session_state.df_before_transformation.copy()
                
                # Create DataNormalizer instance for selected columns only
                subset_normalizer = DataNormalizer(transformed_df[columns_to_transform])
                
                # Apply transformation using DataNormalizer
                transformed_subset = subset_normalizer.transform(method=transformation_method)
                
                # Update only the selected columns
                transformed_df[columns_to_transform] = transformed_subset
                
                # Store transformed DataFrame in session state
                st.session_state.df = transformed_df
                update_session_state()

                with col2:
                    st.write("**Transformed DataFrame:**")
                    st.write(transformed_df)

                    if selected_column:
                        fig_after = go.Figure()
                        fig_after.add_trace(go.Histogram(
                            x=transformed_df[selected_column],
                            nbinsx=50,
                            marker_color='lightgreen',
                            name='Transformed'
                        ))
                        fig_after.update_layout(
                            title=f"Transformed Distribution: {selected_column}",
                            xaxis_title=selected_column,
                            yaxis_title='Count'
                        )
                        st.plotly_chart(fig_after)

                st.success("Data transformed successfully.")

            except Exception as e:
                st.error(f"An unexpected error occurred during transformation: {str(e)}")
                DataNormalizer.log_message(str(e))
    
    # If transformed data exists but button wasn't just clicked, still show it
    elif 'df' in st.session_state and not st.session_state.df.equals(st.session_state.df_before_transformation):
        with col2:
            st.write("**Transformed DataFrame:**")
            st.write(st.session_state.df)

            if selected_column:
                fig_after = go.Figure()
                fig_after.add_trace(go.Histogram(
                    x=st.session_state.df[selected_column],
                    nbinsx=50,
                    marker_color='lightgreen',
                    name='Transformed'
                ))
                fig_after.update_layout(
                    title=f"Transformed Distribution: {selected_column}",
                    xaxis_title=selected_column,
                    yaxis_title='Count'
                )
                st.plotly_chart(fig_after)

def check_data_quality():
    st.markdown("<h2 style='color: #2a98bd;'>Data Quality Assessment</h2>", unsafe_allow_html=True)
    
    df = st.session_state.df
    quality_assessor = st.session_state.quality_assessor
    
    st.write("**Current DataFrame:**")
    st.write(df)
    
    try:
        st.write("### Summary Statistics:")
        summary_stats = quality_assessor.summary_statistics()
        st.write(summary_stats)
    except Exception as e:
        st.error("An unexpected error occurred while assessing data quality.")
        log_error(e)

def main():
    
    if 'page' not in st.session_state:
        st.session_state.page = 'upload'

    if st.session_state.page == 'upload':
        show_header()
        col1,col2,col3=st.columns([1,2,1])
        with col2:
            st.write("Upload a CSV file to start cleaning..")
        upload_file()
    else:
        if 'df' in st.session_state:
            st.sidebar.header("Data Cleaning")
            action = st.sidebar.selectbox("Select Action", [
                "Data Overview",
                "Missing Values",
                "Outliers",
                "Normalize",
                "Transform",
                "Check Data Quality"
            ])

            if action == "Data Overview":
                show_data_overview()
            elif action == "Missing Values":
                handle_missing_values()
            elif action == "Outliers":
                handle_outliers()
            elif action == "Normalize":
                normalize_data()
            elif action == "Transform":
                transform_data()
            elif action == "Check Data Quality":
                check_data_quality()
        else:
            st.write("No data uploaded. Please upload a CSV file first.")

if __name__ == "__main__":
    main()
