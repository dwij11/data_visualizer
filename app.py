import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuration ---
st.set_page_config(page_title="Data Visualizer", page_icon=":bar_chart:", layout="wide")
sns.set_style("whitegrid")
primary_color = "#4CAF50"
secondary_color = "#388E3C"
text_color = "#212121"

# --- Custom CSS ---
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: #f7f7f7;
            color: {text_color};
        }}
        .st-header {{
            background-color: {primary_color};
            color: white;
            padding: 1rem 0;
            border-radius: 0 0 0.5rem 0.5rem;
        }}
        .st-subheader {{
            color: {secondary_color};
        }}
        .st-selectbox > div > div > div > div {{
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 0.25rem;
            color: {text_color};
        }}
        .st-selectbox > div > div > div > div:hover {{
            border-color: {primary_color};
        }}
        .st-button > button {{
            background-color: {primary_color};
            color: white;
            border: none;
            border-radius: 0.3rem;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }}
        .st-button > button:hover {{
            background-color: {secondary_color};
        }}
        .streamlit-expanderHeader {{
            font-weight: bold;
            color: {secondary_color};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Settings")
    github_repo_link = st.sidebar.text_input("GitHub Repo Link (Data Folder):", "https://github.com/dwij11/data_visualizer/tree/main/data")

    file_urls = {}
    if github_repo_link:
        try:
            repo_name = github_repo_link.split('/')[-3]
            base_url = f"https://raw.githubusercontent.com/{repo_name}/main/data/"
            default_files = {
                "diabetes.csv": "diabetes.csv",
                "heart.csv": "heart.csv",
                "parkinsons.csv": "parkinsons.csv",
                "tips.csv": "tips.csv",
                "titanic.csv": "titanic.csv"
            }
            for display_name, filename in default_files.items():
                file_urls[display_name] = base_url + filename
        except:
            st.sidebar.warning("Invalid GitHub link format.")
            file_urls = {
                "diabetes.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/diabetes.csv",
                "heart.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/heart.csv",
                "parkinsons.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/parkinsons.csv",
                "tips.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/tips.csv",
                "titanic.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/titanic.csv"
            }
    else:
        file_urls = {
            "diabetes.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/diabetes.csv",
            "heart.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/heart.csv",
            "parkinsons.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/parkinsons.csv",
            "tips.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/tips.csv",
            "titanic.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/titanic.csv"
        }

    selected_file_display = st.sidebar.selectbox('Select a dataset', list(file_urls.keys()), index=0)
    selected_file = file_urls[selected_file_display].split('/')[-1]

# --- Main Area ---
st.title(':bar_chart: Interactive Data Visualizer')
st.subheader('Explore your data with ease!')

if selected_file:
    file_url = file_urls[selected_file_display]
    with st.spinner(f'Loading data from {selected_file_display}...'):
        response = requests.get(file_url)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            df = pd.read_csv(StringIO(content))
            st.success(f'Data from {selected_file_display} loaded successfully!')

            with st.expander("Show Dataframe"):
                st.dataframe(df)

            st.subheader("Visualize Your Data")
            col1, col2 = st.columns(2)
            with col1:
                x_axis = st.selectbox('Select the X-axis', options=df.columns.tolist() + ["None"])
            with col2:
                y_axis = st.selectbox('Select the Y-axis', options=df.columns.tolist() + ["None"])

            plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
            plot_type = st.selectbox('Select the type of plot', options=plot_list)

            if st.button('Generate Plot'):
                if x_axis == "None" and y_axis == "None":
                    st.warning("Please select at least one axis for plotting.")
                elif x_axis == "None" and plot_type not in ['Distribution Plot', 'Count Plot']:
                    st.warning("Please select an X-axis for this plot type.")
                elif y_axis == "None" and plot_type not in ['Distribution Plot', 'Count Plot']:
                    st.warning("Please select a Y-axis for this plot type.")
                else:
                    with st.spinner('Generating plot...'):
                        fig, ax = plt.subplots(figsize=(8, 5))
                        try:
                            if plot_type == 'Line Plot':
                                sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
                            elif plot_type == 'Bar Chart':
                                sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
                            elif plot_type == 'Scatter Plot':
                                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
                            elif plot_type == 'Distribution Plot':
                                sns.histplot(df[x_axis], kde=True, ax=ax)
                                y_axis_label = 'Density'
                            elif plot_type == 'Count Plot':
                                sns.countplot(x=df[x_axis], ax=ax)
                                y_axis_label = 'Count'

                            # Adjust label sizes and title
                            ax.tick_params(axis='x', labelsize=10)
                            ax.tick_params(axis='y', labelsize=10)
                            if plot_type in ['Distribution Plot', 'Count Plot']:
                                plt.title(f'{plot_type} of {x_axis}', fontsize=14)
                                plt.xlabel(x_axis, fontsize=12)
                                plt.ylabel(y_axis_label, fontsize=12)
                            else:
                                plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=14)
                                plt.xlabel(x_axis, fontsize=12)
                                plt.ylabel(y_axis, fontsize=12)
                            plt.tight_layout()
                            st.pyplot(fig)
                        except KeyError as e:
                            st.error(f"Error: Column '{e}' not found in the dataframe.")
                        except Exception as e:
                            st.error(f"An error occurred while generating the plot: {e}")

        else:
            st.error("Failed to load data from the specified URL.")
else:
    st.info("Please provide a valid GitHub repository link in the sidebar to load datasets.")
