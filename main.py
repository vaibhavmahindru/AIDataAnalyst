import streamlit as st
import pandas as pd
from utils import *

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# deepseek key
deepseekApiKey = st.secrets["deepseek"]["api_key"]

geminiApiKey = st.secrets["gemini"]["geminiApiKey"]
# Page config
st.set_page_config(
    page_title="AI Data Analyst",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("AI Data Analyst")
st.markdown("Upload your **csv/xlsx** file to begin")

# Upload the file
uploadedFile = st.file_uploader(
    "Choose your dataset(csv/xlsx)",
    type=["csv", "xlsx"], 
    key="uploadedData", 
    help="Upload a csv/xlsx file to analyse", 
    disabled=False, 
    label_visibility="visible", 
    accept_multiple_files=False
)
submit = st.button("Submit File")

# Logic after submitting the file

if uploadedFile is not None and submit:
    try:
        fileExtension = uploadedFile.name.split('.')[-1].lower()

        # file format checker
        if fileExtension == 'csv':
            df = pd.read_csv(uploadedFile)
        elif fileExtension == 'xlsx':
            df = pd.read_excel(uploadedFile, engine="openpyxl")
        else:
            st.write("Unsupported file format")
            st.stop()
        
        # save the datset in session storage
        st.session_state['df'] = df
        st.session_state['fileUploaded'] = True

        # col names
        st.session_state['columnNames'] = df.columns.to_list()
        # data type of all the col
        st.session_state['dataTypes'] = df.dtypes.astype(str).reset_index().rename(columns={'index': 'Column', 0: 'Dtype'})
        # no. of missing value per column
        st.session_state['missingValues'] = df.isnull().sum().reset_index().rename(columns={'index': 'Column', 0: 'Missing Values'})
        # more description about the col
        st.session_state['descriptionStats'] = df.describe(include='all').transpose().reset_index().rename(columns={'index': 'col name'})
        # random sample for stats
        st.session_state['sampleRows'] = df.sample(n=min(10, len(df)), random_state=42)
        # correlation matrix of numerical columns only
        st.session_state['correlationMatrix'] = df.corr(numeric_only=True)

        # Find top 4 categorical columns with the most unique values
        catCols = df.select_dtypes(include=['object', 'category']).nunique().sort_values(ascending=False).head(4).index
        catValueCounts = {}
        for col in catCols:
            catValueCounts[col] = df[col].value_counts().head(10).to_dict()
        st.session_state['catValueCounts'] = catValueCounts


        AIPrompt = f"""
        You are a professional data analyst. Based on the dataset provided below, perform an initial data analysis and share your expert insights in a concise and structured way. Your goal is to help stakeholders understand the dataset, identify potential issues, and suggest directions for deeper analysis or business actions.
        ### Dataset Summary

        #### 🔹 Column Names
        {st.session_state['columnNames']}

        #### 🔹 Data Types
        {st.session_state['dataTypes'].to_markdown(index=False)}

        #### 🔹 Descriptive Statistics
        {st.session_state['descriptionStats'].to_markdown(index=False)}

        #### 🔹 Missing Values
        {st.session_state['missingValues'].to_markdown(index=False)}

        #### 🔹 Random Sample Rows
        {st.session_state['sampleRows'].to_markdown(index=False)}

        #### 🔹 Correlation Matrix
        {st.session_state['correlationMatrix'].round(2).to_markdown()}

        #### 🔹 Top Categorical Value Counts
        """
        for col, counts in catValueCounts.items():
            AIPrompt += f"\n\n**{col}**:\n"
            for k, v in counts.items():
                AIPrompt += f"- {k}: {v}\n"
        AIPrompt += """
        ---

        ### Deliverables:
        1. **High-level summary** of the dataset (what it might represent, key fields).
        2. **Notable patterns, trends, or anomalies** in the data.
        3. **Potential data quality issues**, like missing or inconsistent values.
        4. **Suggestions for additional analysis** or visualizations.
        5. **Business insights** that can be drawn from the data.

        Avoid restating the obvious and focus on providing meaningful, analytical insights.
        """

        sampleRowsMarkdown = st.session_state['sampleRows'].to_markdown(index=False)
        graphPrompt = f"""
You are a professional data analyst.

Below is a sample of a dataset in Markdown table format:

{sampleRowsMarkdown}

Assume the full dataset is already loaded as a pandas DataFrame named `df`.

Your task:
- Generate 4 to 5 insightful, interactive visualizations using **Python and Plotly**.
- Use the **entire DataFrame (`df`)** — not just the sample.
- Focus on distributions, trends, comparisons, correlations, or outliers.
- Ensure you only pass **numeric or properly formatted columns** to Plotly Express.
- Convert non-numeric columns if needed (e.g., parse dates, encode categories).
- Each visualization should be in its **own clean, complete code block** with appropriate titles and labels.
- Use Plotly's `express` or `graph_objects` API for interactivity.
- Output only runnable Python code — no markdown, explanations, or comments.
- Ensure axis tick labels, legends, and annotations are readable and do not overlap.
- Use Plotly layout options like `fig.update_layout()` or `fig.update_xaxes(tickangle=45)` where necessary.
- Set reasonable figure size.
- Adjust margins and padding for clear visualization.
- Each chart should be in its own complete code block with readable labels and layout adjustments.
- Before plotting, ensure numeric columns are truly numeric. Use `pd.to_numeric(..., errors="coerce")` if needed.
- Only use column names that actually exist in `df.columns`.
- Avoid hardcoding column names — dynamically explore or print `df.columns` if needed.
- Avoid using newline-wrapped or partially matched column names.
- Write safe, defensive code to skip any columns not found in the DataFrame.
"""

        with st.spinner("🔍 Generating AI Summary and graphs... Please wait..."):
            AISummary = callGeminiSummary(AIPrompt)
            graphCode = callGeminiGraph(graphPrompt)
            st.session_state["AISummary"] = AISummary
            st.session_state["graphCode"] = graphCode

    except Exception as e:
        st.error(f"Something went wrong while reading the file: {e}")

elif submit and uploadedFile is None:
    st.warning("Please upload a file before clicking Submit.")

# ===============================
# Show saved analysis if available
# ===============================
if 'fileUploaded' in st.session_state:
    df = st.session_state['df']
    columnNames = st.session_state['columnNames']
    dataTypes = st.session_state['dataTypes']
    missingValues = st.session_state['missingValues']
    descriptionStats = st.session_state['descriptionStats']
    sampleRows = st.session_state['sampleRows']
    correlationMatrix = st.session_state['correlationMatrix']
    catValueCounts = st.session_state['catValueCounts']

    # collapsable preview of the first 5 rows of the dataset
    with st.expander("Preview of Dataset", expanded=False):
        # preview of the first 5 rows, by default it is 5, enter the required number for specific rows
        st.dataframe(df.head(), use_container_width=True)

    # basic info of the dataset containing things like -- no. of rows and cols, name of all the cols and their types, no. of missing values
    # add other things in future like describe, unique values or incorrect data entry
    with st.expander("Basic Info of the dataset", expanded=False):
        # no of rows
        st.write(f"Rows: {df.shape[0]}")
        # no of cols
        st.write(f"Columns: {df.shape[1]}")
        # col names
        st.write(f"Column Names: {columnNames}")
        # col data types
        st.markdown("#### 🔹 Column Data Types")
        st.dataframe(dataTypes)
        # no. of missing values
        st.markdown("#### 🔹 Missing Values")
        st.dataframe(missingValues)

    if 'AISummary' in st.session_state:
        with st.expander("AI Summary", expanded=False):
            st.markdown("### AI Insights")
            st.markdown(st.session_state['AISummary'])

        st.download_button(
            label="📥 Download AI Summary as .txt",
            data=st.session_state['AISummary'],
            file_name="AI_Summary.txt",
            mime="text/plain"
        )
    
    if 'graphCode' in st.session_state:
        with st.expander("AI-Generated Plotly Code", expanded=False):
            graphCode = st.session_state['graphCode']
            st.code(graphCode, language="python")
        

        if st.button("Run Graph Code"):
            try:
                import uuid  # for generating unique keys
                collected_figures = []
                # Custom wrapper for Plotly, [future] Matplotlib display
                def show_plot(fig=None):
                    if fig:
                        try:
                            collected_figures.append(fig)
                            # unique_key = str(uuid.uuid4())  # generate a unique key
                            # st.plotly_chart(fig, use_container_width=True, key=unique_key)
                        except Exception as e:
                            st.error(f"⚠️ Plotly rendering error: {e}")
                # Execution environment
                exec_env = {
                    'df': df,
                    'st': st,
                    'px': px,
                    'go': go,
                    # 'plt': plt, matplotlib
                    'fig': None,
                    'make_subplots': make_subplots,
                    'show': show_plot
                }

                # Replace fig.show() and plt.show() with custom handler
                cleanedGraphCode = st.session_state['graphCode']
                for i in range(1,10):
                    cleanedGraphCode = cleanedGraphCode.replace(f"fig{i}.show()", f"show(fig{i})")
                cleanedGraphCode = cleanedGraphCode.replace("fig.show()", "show(fig)")

                # Run the AI-generated code safely
                exec(cleanedGraphCode, exec_env)

                # Display all collected figures in one expander
                with st.expander("📊 AI-Generated Graphs", expanded=False):
                    for idx, fig in enumerate(collected_figures, start=1):
                        st.plotly_chart(fig, use_container_width=True, key=f"fig_{idx}_{uuid.uuid4()}")

            except Exception as e:
                st.error(f"Error running AI graph code: {e}")


# ===============================
# Reset Button to clear session
# ===============================
st.markdown("---")
if st.button("🔄 Reset App"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
