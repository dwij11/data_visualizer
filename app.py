import streamlit as st
import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

# GitHub repository link
github_repo_link = "https://github.com/dwij11/data_visualizer/tree/main/data"

# Title
st.title('Data Visualizer')

# Dictionary of CSV file names and their GitHub raw file URLs
file_urls = {
    "diabetes.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/diabetes.csv",
    "heart.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/heart.csv",
    "parkinsons.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/parkinsons.csv",
    "tips.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/tips.csv",
    "titanic.csv": "https://raw.githubusercontent.com/dwij11/data_visualizer/main/data/titanic.csv"
}

# Dropdown to select a file
selected_file = st.selectbox('Select a file', list(file_urls.keys()), index=0)

if selected_file:
    # Read the selected CSV file
    file_url = file_urls[selected_file]
    response = requests.get(file_url)
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        df = pd.read_csv(StringIO(content))

        # Display the DataFrame
        st.write(df.head())

        # Allow the user to select columns for plotting
        x_axis = st.selectbox('Select the X-axis', options=df.columns.tolist() + ["None"])
        y_axis = st.selectbox('Select the Y-axis', options=df.columns.tolist() + ["None"])

        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        # Allow the user to select the type of plot
        plot_type = st.selectbox('Select the type of plot', options=plot_list)

        # Generate the plot based on user selection
        if st.button('Generate Plot'):
            fig, ax = plt.subplots(figsize=(6, 4))
            if plot_type == 'Line Plot':
                sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Bar Chart':
                sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Scatter Plot':
                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Distribution Plot':
                sns.histplot(df[x_axis], kde=True, ax=ax)
                y_axis='Density'
            elif plot_type == 'Count Plot':
                sns.countplot(x=df[x_axis], ax=ax)
                y_axis = 'Count'

            # Adjust label sizes
            ax.tick_params(axis='x', labelsize=10)  # Adjust x-axis label size
            ax.tick_params(axis='y', labelsize=10)  # Adjust y-axis label size

            # Adjust title and axis labels with a smaller font size
            plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
            plt.xlabel(x_axis, fontsize=10)
            plt.ylabel(y_axis, fontsize=10)

            # Show the results
            st.pyplot(fig)

    else:
        st.error("Failed to load data")
