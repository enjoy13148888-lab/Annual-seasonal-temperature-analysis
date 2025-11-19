# Annual-seasonal-temperature-analysis

Introduction & Data

Due to worsening climate change, people pay more attention to daily temperature changes. New Zealand's agriculture and animal husbandry account for about 20% of the GDP and over 65% of exports, making it an important industry to study climate impacts. Therefore, this project uses public environmental data from the New Zealand government to analyze temperature changes from 1909 to 2019, predict future climate trends, and suggest prevention strategies. The data comes from the New Zealand government for the Environment and includes columns such as year, temperature, data_released, source, anomaly, and reference_period, covering both numerical and text formats.


Usage & Code Overview

This project uses an interactive menu with 8 options for users to choose from.
[0]"Temperature Report-Single Year"
[1]"Temperature Over Time Graph"
[2]"Anomaly Over Time Graph"
[3]"Summary of Temperature Statistics"
[4]"Summary of Anomaly Statistics"
[5]"Temperature Boxplot"
[6]"Anomaly Boxplot"
[7]"Exit

In menu option[0] "Temperature Report - Single Year", users can input a year and a data source to look for temperature records for that specific year and source. The function read_csv_data reads the CSV and returns a list of data rows by columns. The functions get_unique_years and get_unique_sources get unique years and sources from the data for input validation. Using try-except blocks prevents the program from crashing if users input wrong data. A while True loop allows users to keep trying until they enter valid information. Menu option [7]"Exit" quits the program. Options[1] to [6] include basic statistical analysis and visualizations and will be explained in the Analysis & Visualization Implementation section.




Analysis & Visualization Implementation

Menu options [1]and[2] have similar functions. They first use read_temperature_data and read_anomaly_data to read CSV files into pandas DataFrames. These functions remove missing values in the temperature or anomaly columns and ensure the column data type is numeric. The cleaned DataFrames are returned for further analysis. Then, plot_temperature_heatmap and plot_anomaly_heatmap functions create heatmaps using seaborn, with year as the row index, source as the column index, and temperature or anomaly as the heatmap values. This allows users to quickly understand data trends.

Menu options[3] and [4] are also similar. They use calc_temperature_stats and calc_anomaly_stats functions with pandas groupby to group data by the source column. Then, they calculate each group's mean, standard deviation, maximum, and minimum values, returning these statistics. Finally, the main program prints titles like "Average temperature" along with the related data for easy user reading.

Menu options [5] and [6] visualize the statistics from options [3] and [4] using box plots. The functions plot_temperature_boxplot and plot_anomaly_boxplot use Plotly Express to create box plots of temperature or anomaly distributions. The x-axis represents the source column, comparing different data sources, and the y-axis shows the values of temperature or anomaly. The interactive plots are displayed with fig.show(), allowing users to intuitively analyze the statistical data.

Dependencies

The project mainly uses pandas for data cleaning, grouping, and basic statistical analysis (such as mean, standard deviation, maximum, and minimum). Seaborn is used to create heatmaps, allowing users to quickly understand changes in the average temperature and anomalies each year. Finally, plotly.express is used to visualize the statistical results as box plots.

Resource
https://data.mfe.govt.nz/table/105056-daily-temperature-1909-2019/


