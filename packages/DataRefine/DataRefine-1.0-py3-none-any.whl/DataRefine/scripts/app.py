import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import logging
import traceback
from DataRefine.handle_missing import MissingDataHandler
from DataRefine.handle_outliers import OutlierHandler
from DataRefine.normalize import DataNormalizer
from DataRefine.data_quality_assessment import DataQualityAssessment
import pkg_resources

# Load application logo from package resources
logo_path = pkg_resources.resource_filename('DataRefine', 'scripts/drlogo.jpeg')

# Configure Streamlit page settings for optimal display
st.set_page_config(
    page_title="DataRefine",
    page_icon=logo_path,
    layout="wide"  # Uses full width of the browser window
)

# Set up application-wide logging configuration
logging.basicConfig(
    level=logging.ERROR,  # Only log error-level messages and above
    format='%(asctime)s %(levelname)s: %(message)s',  # Include timestamp and log level
    handlers=[logging.StreamHandler()]  # Output logs to console
)

def log_error(e):
    """
    Log exceptions with full traceback for debugging purposes.
    
    Args:
        e (Exception): The exception object to be logged
    
    Example:
        try:
            some_function()
        except Exception as e:
            log_error(e)
    """
    logging.error(f"Error: {e}")
    logging.error(traceback.format_exc())

def show_header():
    """
    Display the application header with logo and title.
    
    Creates a three-column layout with the title and logo centered in the middle column.
    The title is styled with a specific blue color (#2a98bd) using HTML/CSS.
    
    Note:
        This function uses st.columns in the ratio [1:2:1] to center the content
        and unsafe_allow_html=True to apply custom styling.
    """
    # Create a three-column layout with wider center column
    col1, col2, col3 = st.columns([1, 2, 1])
    
    # Display title and logo in center column
    with col2:
        # Add custom styled header
        st.markdown("<h1 style='color: #2a98bd;'>DataRefine</h1>", unsafe_allow_html=True)
        # Display logo image
        st.image(logo_path, caption=None, width=200)
        
def upload_file():
   """
   Handle CSV file upload functionality and initialize application state.

   This function creates a centered file upload interface that:
   1. Accepts CSV files only
   2. Loads the data into a pandas DataFrame
   3. Initializes session state with the uploaded data
   4. Provides navigation to the data cleaning page

   The function implements comprehensive error handling for:
   - Empty CSV files
   - Invalid CSV formats
   - General file processing errors

   Returns:
       None

   Raises:
       pd.errors.EmptyDataError: When uploaded CSV file contains no data
       pd.errors.ParserError: When CSV file format is invalid
       Exception: For unexpected errors during file processing

   Example:
       # This function is typically called in a Streamlit app
       if __name__ == "__main__":
           upload_file()

   Note:
       - Uses st.experimental_rerun() for page navigation
       - Modifies st.session_state with uploaded data
       - Displays success/error messages with consistent styling
   """
   # Create a three-column layout with center emphasis
   col1, col2, col3 = st.columns([1, 2, 1])
   
   with col2:
       # Display file uploader widget restricted to CSV files
       uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
       
       # Process the file once uploaded
       if uploaded_file is not None:
           try:
               # Load CSV data into pandas DataFrame
               df = pd.read_csv(uploaded_file)
               
               # Set up session state with the loaded data
               initialize_session_state(df)
               
               # Display success message with consistent brand color
               st.markdown(
                   "<p style='color: #2a98bd;'>File uploaded successfully!</p>", 
                   unsafe_allow_html=True
               )
               
               # Add navigation button to data cleaning interface
               if st.button("Go to Data Cleaning"):
                   st.session_state.page = 'analysis'  # Update navigation state
                   st.experimental_rerun()  # Trigger page refresh
                   
           except pd.errors.EmptyDataError:
               # Handle empty file uploads
               st.error("The uploaded file is empty. Please upload a valid CSV file.")
               
           except pd.errors.ParserError:
               # Handle invalid CSV format
               st.error("The uploaded file could not be parsed. Please ensure it is a valid CSV file.")
               
           except Exception as e:
               # Catch and log any unexpected errors
               st.error("An unexpected error occurred while loading the file.")
               log_error(e)  # Log detailed error information for debugging

def initialize_session_state(df: pd.DataFrame):
   """
   Initialize Streamlit session state with the uploaded DataFrame and create data handler instances.
   
   This function serves as the primary initializer for the application's state,
   storing the DataFrame and triggering the creation of all necessary data handling objects.

   Args:
       df (pd.DataFrame): The DataFrame containing the uploaded CSV data
       
   Note:
       This function modifies st.session_state by:
       1. Storing the input DataFrame
       2. Triggering creation of all data handler instances via update_session_state()
   
   Example:
       >>> df = pd.read_csv('example.csv')
       >>> initialize_session_state(df)
       # Session state now contains DataFrame and all handler instances
   """
   # Store the DataFrame in session state for global access
   st.session_state.df = df
   
   # Initialize all data handlers and tools
   update_session_state()

def update_session_state():
   """
   Create and initialize all data handling objects using the stored DataFrame.
   
   This function instantiates various data handling classes for:
   - Missing data treatment
   - Outlier detection and handling
   - Data normalization
   - Data quality assessment
   
   Each handler is stored in the session state for persistent access across
   the application's lifecycle.

   Dependencies:
       Requires the following custom classes:
       - MissingDataHandler: For handling missing values
       - OutlierHandler: For detecting and treating outliers
       - DataNormalizer: For data normalization operations
       - DataQualityAssessment: For assessing data quality metrics

   Session State Modified:
       - handler: Instance of MissingDataHandler
       - outlier_handler: Instance of OutlierHandler
       - normalizer: Instance of DataNormalizer
       - quality_assessor: Instance of DataQualityAssessment

   Note:
       Assumes st.session_state.df contains a valid pandas DataFrame
   
   Raises:
       AttributeError: If st.session_state.df is not initialized
       Exception: If any handler initialization fails
   """
   try:
       # Retrieve DataFrame from session state
       df = st.session_state.df
       
       # Initialize missing data handler
       st.session_state.handler = MissingDataHandler(df)
       
       # Initialize outlier detection and handling
       st.session_state.outlier_handler = OutlierHandler(df)
       
       # Initialize data normalization tools
       st.session_state.normalizer = DataNormalizer(df)
       
       # Initialize data quality assessment tools
       st.session_state.quality_assessor = DataQualityAssessment(df)
       
   except AttributeError:
       raise AttributeError("DataFrame not found in session state. Please ensure initialize_session_state() is called first.")
   except Exception as e:
       log_error(e)
       raise Exception("Failed to initialize one or more data handlers. Check logs for details.")

def show_data_overview():
   """
   Display a comprehensive overview of the loaded DataFrame in Streamlit.
   
   This function creates a structured display of the dataset information including:
   1. Dataset dimensions (rows × columns)
   2. Full DataFrame preview
   3. Detailed column information:
       - Column names
       - Data types
       - Non-null value counts

   The column information is reformatted from pandas info() output into a 
   more readable table format.

   Dependencies:
       - pandas
       - streamlit
       - io.StringIO for capturing pandas info() output

   Session State Required:
       - st.session_state.df: pandas DataFrame containing the loaded data

   Raises:
       Exception: If there's an error processing or displaying the data information
       
   Note:
       - Column names are cleaned by removing leading numbers
       - The display uses consistent styling with the app's color theme (#2a98bd)
       - Info table excludes header and footer lines from pandas info()
   """
   # Display section header with consistent styling
   st.markdown("<h2 style='color: #2a98bd;'>Data Overview</h2>", unsafe_allow_html=True)
   
   # Get DataFrame from session state
   df = st.session_state.df
   
   # Display basic DataFrame information
   st.write("**Data Shape:**", df.shape)
   st.write("**DataFrame:**", df)
   
   # Process and display detailed column information
   st.write("**Data Information:**")
   buffer = io.StringIO()
   
   try:
       # Capture DataFrame info output in buffer
       df.info(buf=buffer)
       buffer.seek(0)  # Reset buffer position to start
       
       # Extract relevant lines from info output
       info_lines = buffer.getvalue().splitlines()
       data_lines = info_lines[5:-2]  # Skip header and footer lines
       
       if data_lines:
           # Parse and format column information
           table_data = []
           for line in data_lines:
               parts = line.split()
               if len(parts) >= 3:
                   # Extract and format column information
                   column = ' '.join(parts[:-2])
                   non_null_count = parts[-2] + ' ' + parts[-1]
                   dtype = parts[-3]
                   
                   # Clean column names by removing leading numbers
                   column = ' '.join(part.lstrip('0123456789') 
                                   for part in column.split())
                   
                   # Add formatted data to table
                   table_data.append([column, non_null_count, dtype])
           
           # Create and display formatted table
           table_df = pd.DataFrame(
               table_data, 
               columns=["Column", "Dtype", "Non-Null Count"]
           )
           st.write(table_df)
           
   except Exception as e:
       # Handle and log any errors during processing
       st.error("An error occurred while displaying data information.")
       log_error(e)

def handle_missing_values():
   """
   Provide an interactive interface for detecting and handling missing values in the dataset.
   
   This function creates a comprehensive missing value handling interface that:
   1. Displays side-by-side comparison of original and imputed data
   2. Provides interactive selection of columns and imputation strategies
   3. Visualizes missing value patterns using plotly charts
   4. Performs imputation on selected columns with chosen strategy
   
   Features:
   - Multiple imputation strategies: mean, median, most_frequent, predictive, custom
   - Column-specific imputation
   - Visual comparison of before/after states
   - Missing values visualization
   - Persistent state management
   
   Session State Modified:
       - df_before_imputation: Original DataFrame before any imputation
       - df: Updated DataFrame after imputation
       - handler: MissingDataHandler instance updated after imputation
   
   Dependencies:
       - streamlit
       - plotly (for visualizations)
       - MissingDataHandler class for imputation operations
   
   Note:
       The function preserves the original data for comparison and
       only updates selected columns during imputation.
   
   Raises:
       Exception: For any errors during the imputation process
   """
   # Display section header with consistent styling
   st.markdown("<h2 style='color: #2a98bd;'>Missing Values Detection and Handling</h2>", 
               unsafe_allow_html=True)
   
   # Initialize original data storage if not exists
   if 'df_before_imputation' not in st.session_state:
       st.session_state.df_before_imputation = st.session_state.df.copy()
   
   # Create layout for before/after comparison
   col1, col2 = st.columns(2)
   
   # Get handler instance from session state
   handler = st.session_state.handler
   
   # Display original data and missing values visualization
   with col1:
       st.write("**Original DataFrame with Missing Values:**")
       st.write(st.session_state.df_before_imputation)
       
       # Visualize original missing value patterns
       st.plotly_chart(handler.plot_missing_values(st.session_state.df_before_imputation))

   # Setup sidebar controls for imputation
   st.sidebar.write("### Handle Missing Values")
   
   # Column selection interface
   columns = st.sidebar.multiselect(
       "Select Columns for Imputation",
       options=st.session_state.df_before_imputation.columns.tolist(),
       default=st.session_state.df_before_imputation.columns.tolist()
   )
   
   # Imputation strategy selection
   strategy = st.sidebar.selectbox(
       "Select Imputation Strategy",
       ["mean", "median", "most_frequent", "predictive", "custom"]
   )
   
   # Custom value input if selected
   fill_value = None
   if strategy == "custom":
       fill_value = st.sidebar.text_input("Fill Value", value="0")

   # Handle imputation process
   if st.sidebar.button("Impute Missing Values"):
       with st.spinner("Imputing missing values..."):
           try:
               # Validate column selection
               if not columns:
                   st.warning("No columns selected for imputation. Please select at least one column.")
                   return
               
               # Prepare data for imputation
               df_imputed = st.session_state.df_before_imputation.copy()
               df_subset = df_imputed[columns].copy()
               
               # Perform imputation on selected columns
               df_imputed_subset = handler.impute_missing(
                   strategy, 
                   fill_value=fill_value, 
                   dataframe=df_subset
               )
               
               # Update imputed columns in full DataFrame
               df_imputed[columns] = df_imputed_subset
               
               # Update session state with imputed data
               st.session_state.df = df_imputed
               update_session_state()
               
               # Display imputed data and visualization
               with col2:
                   st.write("**DataFrame After Imputation:**")
                   st.write(df_imputed)
                   st.plotly_chart(handler.plot_missing_values(df_imputed))
               
               st.success("Missing values imputed successfully.")
               
           except Exception as e:
               st.error("An unexpected error occurred during imputation.")
               log_error(e)
   
   # Display current imputed data if it exists
   elif 'df' in st.session_state and not st.session_state.df.equals(st.session_state.df_before_imputation):
       with col2:
           st.write("**DataFrame After Imputation:**")
           st.write(st.session_state.df)
           st.plotly_chart(handler.plot_missing_values(st.session_state.df))

def handle_outliers():
   """
   Provide an interactive interface for detecting and handling outliers in the dataset.
   
   This function creates a comprehensive outlier analysis dashboard that includes:
   1. Side-by-side comparison of original and processed data
   2. Interactive outlier detection configuration
   3. Visual analysis using box plots
   4. Multiple outlier handling strategies
   
   Features:
   - Detection Methods:
       * IQR (Interquartile Range) with customizable threshold
       * Z-score with customizable threshold
   - Handling Strategies:
       * Capping: Replace outliers with threshold values
       * Removal: Delete rows containing outliers
       * Imputation: Replace outliers with median values
   - Visual Analysis:
       * Interactive box plots for selected columns
       * Before/after comparison visualization
       
   Session State Modified:
       - df_before_outlier_handling: Original DataFrame preserved for comparison
       - df: Updated DataFrame after outlier handling
       - outlier_handler: Updated OutlierHandler instance
       
   Dependencies:
       - streamlit
       - plotly.graph_objects (go)
       - OutlierHandler class for detection and handling operations
       
   Note:
       The function maintains the original data for comparison and
       provides real-time visual feedback for outlier analysis.
   
   Raises:
       Exception: For errors in outlier detection or handling process
   """
   # Display section header
   st.markdown("<h2 style='color: #2a98bd;'>Outlier Detection and Handling</h2>", 
               unsafe_allow_html=True)
   
   # Initialize/retrieve original data
   if 'df_before_outlier_handling' not in st.session_state:
       st.session_state.df_before_outlier_handling = st.session_state.df.copy()
   
   # Setup layout
   col1, col2 = st.columns(2)
   
   # Display original data (left column)
   with col1:
       st.write("**Original DataFrame:**")
       st.write(st.session_state.df_before_outlier_handling)
   
   # Get handler instance
   outlier_handler = st.session_state.outlier_handler
   
   # Configure outlier detection parameters
   st.sidebar.write("### Outlier Detection Options")
   method = st.sidebar.selectbox(
       "Select Outlier Detection Method", 
       ["iqr", "zscore"],
       index=0,
       help="IQR: Interquartile Range method\nZ-score: Standard deviation based method"
   )
   
   # Set appropriate default threshold based on method
   default_threshold = 1.5 if method == "iqr" else 3.0
   threshold = st.sidebar.slider(
       "Select Threshold", 
       0.0, 5.0, default_threshold, 0.1,
       help="IQR method: Typically use 1.5 (default) or 3.0\nZ-score method: Typically use 3.0"
   )
   
   try:
       # Perform outlier detection
       outliers_df, outlier_counts = outlier_handler.detect_outliers(
           method=method,
           threshold=threshold
       )
       
       # Get numerical columns for visualization
       numerical_columns = st.session_state.df_before_outlier_handling.select_dtypes(
           include=['number']
       ).columns.tolist()
       
       # Column selection for visualization
       selected_column = st.sidebar.selectbox(
           "Select Column to see Box Plot Distribution",
           options=numerical_columns
       )
       
       # Display original distribution
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
       
       # Outlier handling configuration
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
       
       # Handle outlier processing request
       if st.sidebar.button("Handle Outliers"):
           with st.spinner("Handling outliers..."):
               try:
                   # Process outliers
                   df_handled, old_counts, new_counts = outlier_handler.handle_outliers(
                       method=handling_method,
                       detection_method=method,
                       threshold=threshold
                   )
                   
                   # Update application state
                   st.session_state.df = df_handled
                   update_session_state()
                   
                   # Display results
                   with col2:
                       st.write("**DataFrame After Outlier Handling:**")
                       st.write(df_handled)
                       
                       # Show updated distribution
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
       
       # Display current results if they exist
       elif 'df' in st.session_state and not st.session_state.df.equals(
               st.session_state.df_before_outlier_handling):
           with col2:
               st.write("**DataFrame After Outlier Handling:**")
               st.write(st.session_state.df)
               
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
    """
    Creates an interactive Streamlit interface for data normalization with visualization capabilities.
    
    This function provides a user interface for:
    - Selecting normalization method (minmax, zscore, or robust scaling)
    - Choosing numeric columns to normalize
    - Visualizing distributions before and after normalization
    - Comparing original and normalized data side by side
    
    The function uses session state to maintain data persistence between reruns:
    - st.session_state.df_before_normalization: Stores the original DataFrame
    - st.session_state.df: Stores the current (potentially normalized) DataFrame
    - st.session_state.normalizer: Instance of DataNormalizer class
    
    Returns:
        None
    
    Raises:
        Exception: If normalization fails, displays error in Streamlit UI
    
    Note:
        - The function assumes the existence of a DataNormalizer class
        - Requires plotly.graph_objects for visualization
        - Requires streamlit for UI components
        - Uses update_session_state() and log_error() utility functions
    """
    # Display header with custom styling
    st.markdown("<h2 style='color: #2a98bd;'>Data Normalization</h2>", unsafe_allow_html=True)

    # Initialize session state for data persistence
    if 'df_before_normalization' not in st.session_state:
        st.session_state.df_before_normalization = st.session_state.df.copy()

    # Create layout with two columns for before/after comparison
    col1, col2 = st.columns(2)
    
    # Display original data in left column
    with col1:
        st.write("**Original DataFrame:**")
        st.write(st.session_state.df_before_normalization)
    
    # Get normalizer instance from session state
    normalizer = st.session_state.normalizer

    # Sidebar controls for normalization parameters
    st.sidebar.write("### Normalization Options")
    normalization_method = st.sidebar.selectbox("Select Normalization Method", ["minmax", "zscore", "robust"])
    
    # Only show numeric columns as options for normalization
    columns_to_normalize = st.sidebar.multiselect(
        "Select Columns to Normalize",
        options=st.session_state.df_before_normalization.select_dtypes(include=['number']).columns.tolist(),
        default=st.session_state.df_before_normalization.select_dtypes(include=['number']).columns.tolist()
    )

    # Column selection for distribution visualization
    selected_column = st.sidebar.selectbox(
        "Select Column to Plot", 
        options=columns_to_normalize if columns_to_normalize else []
    )

    # Display distribution plot for original data
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

    # Normalization process triggered by button click
    if st.sidebar.button("Apply Normalization"):
        with st.spinner("Normalizing data..."):
            try:
                # Validate input data
                if st.session_state.df_before_normalization is None or st.session_state.df_before_normalization.empty:
                    st.error("The DataFrame is empty or None. Please check if data was loaded correctly.")
                    return

                if not columns_to_normalize:
                    st.warning("No columns selected for normalization. Please select at least one column.")
                    return

                # Perform normalization on selected columns
                normalized_df = st.session_state.df_before_normalization.copy()
                temp_df = normalized_df[columns_to_normalize].copy()
                temp_normalizer = DataNormalizer(temp_df)
                normalized_columns = temp_normalizer.normalize(method=normalization_method)
                
                # Update normalized columns in the full DataFrame
                for col in columns_to_normalize:
                    normalized_df[col] = normalized_columns[col]

                # Update session state with normalized data
                st.session_state.df = normalized_df
                update_session_state()

                # Display normalized data and distribution
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
    
    # Display existing normalized data if available
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
    """
    Creates an interactive Streamlit interface for data transformation with visualization capabilities.
    
    This function provides a user interface for applying various data transformation methods:
    - log transformation: natural logarithm transformation (useful for right-skewed data)
    - sqrt transformation: square root transformation (reduces right skewness less aggressively than log)
    - boxcox transformation: power transformation that optimizes for normality
    
    The interface allows users to:
    - Select transformation method
    - Choose columns to transform
    - Visualize distributions before and after transformation
    - Compare original and transformed data side by side
    
    Session State Variables:
        df_before_transformation (pd.DataFrame): Original DataFrame before transformation
        df (pd.DataFrame): Current (potentially transformed) DataFrame
    
    Dependencies:
        - streamlit (st): For creating the interactive UI
        - plotly.graph_objects (go): For visualization
        - DataNormalizer: Custom class for handling transformations
    
    Returns:
        None
    
    Raises:
        ValueError: If DataNormalizer initialization fails
        Exception: For any unexpected errors during transformation
    
    Notes:
        - Transformations are applied only to selected columns
        - Original data is preserved in session state
        - Visualizations include histograms for distribution comparison
        - Uses update_session_state() utility function to maintain state
    """
    # Display header with custom styling
    st.markdown("<h2 style='color: #2a98bd;'>Data Transformation</h2>", unsafe_allow_html=True)
    
    # Initialize session state with original data if not already stored
    if 'df_before_transformation' not in st.session_state:
        st.session_state.df_before_transformation = st.session_state.df.copy()
    
    # Create layout with two columns for side-by-side comparison
    col1, col2 = st.columns(2)
    
    # Display original data in left column
    with col1:
        st.write("**Original DataFrame:**")
        st.write(st.session_state.df_before_transformation)
    
    # Setup transformation options in sidebar
    st.sidebar.write("### Transformation Options")
    
    # Initialize DataNormalizer with error handling
    try:
        normalizer = DataNormalizer(st.session_state.df_before_transformation)
    except ValueError as e:
        st.error(str(e))
        return
    
    # Transformation method selection
    transformation_method = st.sidebar.selectbox(
        "Select Transformation Method",
        ["log", "sqrt", "boxcox"]  # Available transformation methods
    )
    
    # Column selection for transformation
    columns_to_transform = st.sidebar.multiselect(
        "Select Columns to Transform",
        options=normalizer.dataframe.columns.tolist(),
        default=normalizer.dataframe.columns.tolist()
    )
    
    # Column selection for distribution visualization
    selected_column = st.sidebar.selectbox(
        "Select Column to Plot",
        options=columns_to_transform if columns_to_transform else []
    )

    # Display original distribution plot
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

    # Handle transformation process
    if st.sidebar.button("Apply Transformation"):
        with st.spinner("Transforming data..."):
            try:
                # Validate column selection
                if not columns_to_transform:
                    st.warning("No columns selected for transformation. Please select at least one column.")
                    return

                # Prepare data for transformation
                transformed_df = st.session_state.df_before_transformation.copy()
                subset_normalizer = DataNormalizer(transformed_df[columns_to_transform])
                
                # Apply selected transformation method
                transformed_subset = subset_normalizer.transform(method=transformation_method)
                
                # Update transformed columns in the full DataFrame
                transformed_df[columns_to_transform] = transformed_subset
                
                # Update session state with transformed data
                st.session_state.df = transformed_df
                update_session_state()

                # Display transformed data and distribution
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
    
    # Display existing transformed data if available
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
    """
    Performs and displays a comprehensive data quality assessment using Streamlit UI.
    
    This function provides a data quality report including:
    - Basic dataset information
    - Summary statistics for numerical columns
    - Data quality metrics from the QualityAssessor class
    
    Session State Requirements:
        df (pd.DataFrame): The current DataFrame being analyzed
        quality_assessor (QualityAssessor): Instance of QualityAssessor class
    
    Dependencies:
        - streamlit (st): For creating the interactive UI
        - QualityAssessor: Custom class for data quality assessment
        - log_error: Utility function for error logging
    
    Returns:
        None
    
    Raises:
        Exception: Handles and displays any errors during quality assessment
    """
    # Display section header with custom styling
    st.markdown("<h2 style='color: #2a98bd;'>Data Quality Assessment</h2>", unsafe_allow_html=True)
    
    # Get current DataFrame and quality assessor from session state
    df = st.session_state.df
    quality_assessor = st.session_state.quality_assessor
    
    # Display current DataFrame
    st.write("**Current DataFrame:**")
    st.write(df)
    
    # Generate and display summary statistics with error handling
    try:
        st.write("### Summary Statistics:")
        summary_stats = quality_assessor.summary_statistics()
        st.write(summary_stats)
    except Exception as e:
        st.error("An unexpected error occurred while assessing data quality.")
        log_error(e)


def main():
    """
    Main application function that serves as the entry point for the Streamlit data cleaning app.
    
    This function manages:
    1. Application state and navigation
    2. File upload functionality
    3. Different data cleaning operations through a sidebar menu
    
    Application Sections:
    - Data Upload: Initial page for file upload
    - Data Overview: Basic data exploration
    - Missing Values: Tools for handling missing data
    - Outliers: Outlier detection and treatment
    - Normalize: Data normalization operations
    - Transform: Data transformation operations
    - Data Quality: Quality assessment tools
    
    Session State Variables:
        page (str): Current page/state of the application
        df (pd.DataFrame): The dataset being processed
    
    Dependencies:
        - streamlit (st): For creating the web application
        - Various utility functions for different operations
        
    Notes:
        - The application follows a single-page architecture with different sections
        - All data processing is done in-memory using session state
        - Each operation maintains its own state and can be revisited
    """
    # Initialize application state if first run
    if 'page' not in st.session_state:
        st.session_state.page = 'upload'

    # Handle upload page
    if st.session_state.page == 'upload':
        show_header()
        # Center the upload message using columns
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.write("Upload a CSV file to start cleaning..")
        upload_file()
    else:
        # Main application logic after file upload
        if 'df' in st.session_state:
            # Setup sidebar navigation
            st.sidebar.header("Data Cleaning")
            action = st.sidebar.selectbox("Select Action", [
                "Data Overview",
                "Missing Values",
                "Outliers",
                "Normalize",
                "Transform",
                "Check Data Quality"
            ])

            # Route to appropriate function based on selected action
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
            # Handle case when no data is loaded
            st.write("No data uploaded. Please upload a CSV file first.")


if __name__ == "__main__":
    main()