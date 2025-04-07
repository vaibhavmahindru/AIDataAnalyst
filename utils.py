import requests
import streamlit as st
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel
import re

geminiApiKey = st.secrets["gemini"]["geminiApiKey"]




def extract_code_from_response(text):
    code_match = re.search(r"```python(.*?)```", text, re.DOTALL)
    return code_match.group(1).strip() if code_match else text


configure(api_key=geminiApiKey)

# Initialize Gemini model (gemini-pro is best for text tasks)
model = GenerativeModel(model_name="gemini-1.5-pro")

# Function to get AI summary
def callGeminiSummary(prompt):
    try:
        # return "This is a test AI summary for testing purposes."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"

def callGeminiGraph(prompt):
    try:
        # return "This is a test AI summary for testing purposes."
        graphCodeResponse = model.generate_content(prompt)
        return extract_code_from_response(graphCodeResponse.text)
    except Exception as e:
        return f"❌ Error: {e}"



# def callGeminiGraph(prompt):
#     try:
#         # 🔒 Hardcoded full graph code
#         hardcoded_code = '''
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# # Assuming df is already loaded

# df.columns = [
#     "Student Number", "Last Name", "First Name", "Art of Thinking", "Nature's Machines",
#     "Microeconomics", "Physical World", "Math of Uncertainty", "Communication Lab",
#     "Programming", "Marks*Credits", "Credits", "CGPA"
# ]


# fig1 = px.histogram(df, x="CGPA", nbins=20, title="Distribution of CGPA",
#                    labels={"CGPA": "Cumulative Grade Point Average"})
# fig1.update_layout(bargap=0.1)


# fig2 = px.scatter(df, x="Art of Thinking", y="CGPA", trendline="ols", 
#                  title="Correlation between 'Art of Thinking' and CGPA",
#                  labels={"Art of Thinking": "The Art of Thinking and Reasoning"})



# subject_cols = ["Art of Thinking", "Nature's Machines", "Microeconomics", "Physical World",
#                 "Math of Uncertainty", "Communication Lab", "Programming"]
# fig3 = go.Figure()
# for col in subject_cols:
#     fig3.add_trace(go.Box(y=df[col], name=col))
# fig3.update_layout(title="Distribution of Grades Across Subjects", yaxis_title="Grade")



# fig4 = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])

# grade_counts = pd.cut(df['CGPA'], bins=[0, 6, 7, 8, 9, 10], 
#                       labels=['<6', '6-7', '7-8', '8-9', '9-10']).value_counts()
# fig4.add_trace(go.Pie(labels=grade_counts.index, values=grade_counts.values, title="CGPA Ranges"), row=1, col=1)


# top_bottom_students = pd.concat([df.nlargest(5, 'CGPA'), df.nsmallest(5, 'CGPA')])
# fig4.add_trace(go.Pie(labels=top_bottom_students['First Name'] + ' ' + top_bottom_students['Last Name'], 
#                      values=top_bottom_students['CGPA'], 
#                      title="CGPA of Top and Bottom 5 Students",
#                      textinfo='label+value'), row=1, col=2)

# fig4.update_traces(textposition='inside', hole=.4, hoverinfo="label+percent+name")


# fig5 = px.scatter_matrix(df, dimensions=subject_cols, color="CGPA", 
#                         title="Correlation Matrix of Subject Grades",
#                         labels={col: col.replace(" ", "<br>") for col in subject_cols})  # Improved labels for readability
# fig5.update_traces(diagonal_visible=False, showupperhalf=False)  # Removes redundant information

# fig1.show()
# fig2.show()
# fig3.show()
# fig4.show()
# fig5.show()
# '''
#         return hardcoded_code.strip()
    
#     except Exception as e:
#         return f"❌ Error: {e}"