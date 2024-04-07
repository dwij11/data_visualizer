import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title('Data Visualizer')

# Specify the folder where your CSV files are located
folder_path = r"D:\data-vizualizer-streamlit-web-app-main\data"  # Update this to your folder path

# List all files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Dropdown to select a file
selected_file = st.selectbox('Select a file', files, index=0)

if selected_file:
    # Construct the full path to the file
    file_path = os.path.join(folder_path, selected_file)

    # Read the selected CSV file
    df = pd.read_csv(file_path)

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
