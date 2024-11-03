import streamlit as st
import pandas as pd
from DataRefine.handle_missing import MissingDataHandler
from DataRefine.handle_outliers import OutlierHandler
from DataRefine.normalize import DataNormalizer
from DataRefine.data_quality_assessment import DataQualityAssessment
import plotly.graph_objects as go
import io
import logging
import traceback
import numpy as np
import pkg_resources

logo_path = pkg_resources.resource_filename('DataRefine', 'scripts/drlogo.jpeg')
st.set_page_config(
    page_title="DataRefine",
    page_icon=logo_path,
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

# Page 1: Project Name, Logo, and CSV Upload
def show_upload_page():
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='color: #2a98bd;'>DataRefine</h1>", unsafe_allow_html=True)
        st.image(logo_path, caption=None, width=200) 
    
    st.write("Upload a CSV file to start cleaning..")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.session_state.handler = MissingDataHandler(df)
            st.session_state.outlier_handler = OutlierHandler(df)
            st.session_state.normalizer = DataNormalizer(df)
            st.session_state.quality_assessor = DataQualityAssessment(df)
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

# Page 2: Data Cleaning
def show_analysis_page():
    
    
    if 'df' in st.session_state:
        df = st.session_state.df
        handler = MissingDataHandler(df)
        outlier_handler = OutlierHandler(df)
        normalizer = DataNormalizer(df)
        quality_assessor = DataQualityAssessment(df)
        
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        
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
            st.markdown("<h2 style='color: #2a98bd;'>Data Overview</h2>", unsafe_allow_html=True)
            st.write("**Data Shape:**")
            st.write(df.shape)
            
            st.write("**Dataframe:**")
            st.write(df)
            
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
        
        elif action == "Missing Values":
            st.markdown("<h2 style='color: #2a98bd;'>Missing Values Detection and Handling</h2>", unsafe_allow_html=True)
            
            st.write("**DataFrame with Missing Values**")
            st.write(df)
            
            st.plotly_chart(handler.plot_missing_values(df))
            
            st.sidebar.write("### Handle Missing Values")
            columns = st.sidebar.multiselect("Select Columns for Imputation", options=df.columns.tolist(), default=df.columns.tolist())
            strategy = st.sidebar.selectbox("Select Imputation Strategy", ["mean", "median", "most_frequent", "predictive", "custom"])
            fill_value = None
            if strategy == "custom":
                fill_value = st.sidebar.text_input("Fill Value", value="0")
    
            if st.sidebar.button("Impute Missing Values"):
                with st.spinner("Imputing missing values..."):
                    try:
                        df_subset = df[columns].copy() if columns else df.copy()
                        df_imputed = handler.impute_missing(strategy, fill_value=fill_value, dataframe=df_subset)
                        if columns:
                            df[columns] = df_imputed
                        else:
                            df = df_imputed
                        st.session_state.df = df
                        
                        st.write("### DataFrame After Imputation:")
                        st.write(df)
                        st.plotly_chart(handler.plot_missing_values(df))
                        st.success("Missing values imputed successfully.")
                    except ValueError as e:
                        st.error(f"Value error during imputation: {e}")
                        log_error(e)
                    except KeyError as e:
                        st.error(f"Key error during imputation: {e}")
                        log_error(e)
                    except Exception as e:
                        st.error("An unexpected error occurred during imputation.")
                        log_error(e)
        
        elif action == "Outliers":
            st.markdown("<h2 style='color: #2a98bd;'>Outlier Detection and Handling</h2>", unsafe_allow_html=True)
            method = st.sidebar.selectbox("Select Outlier Detection Method", ["zscore", "iqr", "isolation_forest", "lof"])
            threshold = st.sidebar.slider("Select Threshold", 0.0, 5.0, 3.0, 0.1)
            
            try:
                st.write("**Original DataFrame:**")
                st.write(df)

                outliers_df, outlier_counts = outlier_handler.detect_outliers(method=method, threshold=threshold)
                
                st.plotly_chart(outlier_handler.plot_outliers(outlier_counts))
                
                st.sidebar.write("### Handle Outliers")
                handling_method = st.sidebar.selectbox("Select Outlier Handling Method", ["remove", "cap", "impute"])
                
                if st.sidebar.button("Handle Outliers"):
                    with st.spinner("Handling outliers..."):
                        try:
                            df_handled, old_outlier_counts, new_outlier_counts = outlier_handler.handle_outliers(
                                method=handling_method,
                                detection_method=method,
                                threshold=threshold
                            )
                            # Update the main DataFrame in session state with the handled DataFrame
                            st.session_state.df = df_handled
                            
                            st.write("### DataFrame After Outlier Handling:")
                            st.write(df_handled)
                            
                            st.write("### Outlier Counts After Handling:")
                            new_outlier_counts_df = pd.DataFrame(list(new_outlier_counts.items()), columns=['Column', 'Outlier Count'])
                            st.write(new_outlier_counts_df)
                            
                            st.plotly_chart(outlier_handler.plot_outliers(new_outlier_counts))
                            st.success("Outliers handled successfully.")
                        except ValueError as e:
                            st.error(f"Value error during outlier handling: {e}")
                            log_error(e)
                        except KeyError as e:
                            st.error(f"Key error during outlier handling: {e}")
                            log_error(e)
                        except Exception as e:
                            st.error("An unexpected error occurred during outlier handling.")
                            log_error(e)
            except Exception as e:
                st.error("An unexpected error occurred while detecting outliers.")
                log_error(e)
        
        elif action == "Normalize":
            st.markdown("<h2 style='color: #2a98bd;'>Data Normalization</h2>", unsafe_allow_html=True)
            
            df = st.session_state.df
            
            if 'normalized_df' not in st.session_state:
                st.session_state.normalized_df = df.copy()
            
            normalized_df = st.session_state.normalized_df
            
            st.write("**DataFrame to Normalize:**")
            st.write(normalized_df)
            
            normalizer = DataNormalizer(normalized_df)
            
            st.sidebar.write("### Normalization Options")
            normalization_method = st.sidebar.selectbox("Select Normalization Method", ["minmax", "zscore", "robust"])
            columns_to_normalize = st.sidebar.multiselect(
                "Select Columns to Normalize",
                options=normalizer.dataframe.columns.tolist(),
                default=normalizer.dataframe.columns.tolist()
            )
            
            if st.sidebar.button("Apply Normalization"):
                with st.spinner("Normalizing data..."):
                    try:
                        normalized_df = normalizer.normalize(columns=columns_to_normalize, method=normalization_method)
                        st.session_state.normalized_df = normalized_df
                        st.write("### DataFrame After Normalization:")
                        st.write(normalized_df)
                        st.success("Data normalized successfully.")
                    except ValueError as e:
                        st.error(f"Value error during normalization: {e}")
                        log_error(e)
                    except KeyError as e:
                        st.error(f"Key error during normalization: {e}")
                        log_error(e)
                    except Exception as e:
                        st.error("An unexpected error occurred during normalization.")
                        log_error(e)
        
        elif action == "Transform":
            st.markdown("<h2 style='color: #2a98bd;'>Data Transformation</h2>", unsafe_allow_html=True)
            
            df = st.session_state.df
            
            if 'transformed_df' not in st.session_state:
                st.session_state.transformed_df = df.copy()
            
            transformed_df = st.session_state.transformed_df
            
            st.write("**DataFrame to Transform:**")
            st.write(transformed_df)
            
            transformation_type = st.sidebar.selectbox("Select Transformation Type", ["log", "sqrt", "boxcox"])
            columns_to_transform = st.sidebar.multiselect(
                "Select Columns to Transform",
                options=transformed_df.columns.tolist(),
                default=transformed_df.columns.tolist()
            )
            
            if st.sidebar.button("Apply Transformation"):
                with st.spinner("Transforming data..."):
                    try:
                        # Ensure transformation methods exist
                        if transformation_type == "log":
                            transformed_df = transformed_df.apply(lambda x: np.log1p(x) if x.name in columns_to_transform else x)
                        elif transformation_type == "sqrt":
                            transformed_df = transformed_df.apply(lambda x: np.sqrt(x) if x.name in columns_to_transform else x)
                        elif transformation_type == "boxcox":
                            from scipy import stats
                            transformed_df = transformed_df.apply(
                                lambda x: stats.boxcox(x)[0] if x.name in columns_to_transform and (x > 0).all() else x
                            )
                        st.session_state.transformed_df = transformed_df
                        st.write("### DataFrame After Transformation:")
                        st.write(transformed_df)
                        st.success("Data transformed successfully.")
                    except ValueError as e:
                        st.error(f"Value error during transformation: {e}")
                        log_error(e)
                    except KeyError as e:
                        st.error(f"Key error during transformation: {e}")
                        log_error(e)
                    except Exception as e:
                        st.error("An unexpected error occurred during transformation.")
                        log_error(e)
        
        elif action == "Check Data Quality":
            st.markdown("<h2 style='color: #2a98bd;'>Data Quality Assessment</h2>", unsafe_allow_html=True)
            st.write("**Data Quality Summary:**")
            
            try:
                quality_assessment = DataQualityAssessment(st.session_state.df)
                summary_statistics = quality_assessment.summary_statistics()
                quality_metrics = quality_assessment.quality_metrics()
                
                st.write("**Summary Statistics:**")
                st.write(summary_statistics)
                
                st.write("**Quality Metrics:**")
                st.write(quality_metrics)
            except Exception as e:
                st.error("An unexpected error occurred during data quality assessment.")
                log_error(e)
        
    else:
        st.error("No data found. Please upload a CSV file.")

# Main logic
def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'upload'
    
    if st.session_state.page == 'upload':
        show_upload_page()
    elif st.session_state.page == 'analysis':
        show_analysis_page()
    
if __name__ == "__main__":
    main()
