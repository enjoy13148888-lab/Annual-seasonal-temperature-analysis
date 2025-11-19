import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os

base_dir = os.path.dirname(os.path.abspath(__file__))  
DATA_FILE = os.path.join(base_dir, "annual_and_seasonal_temperature_national_timeseriescsv.csv")


def read_csv_data(filename: str, columns: list[str]) -> list[tuple]:
    """
    Reads in data from a CSV file.
    Returns columns of data requested, in the order given in the columns parameter.
    """
    df = pd.read_csv(filename)
    desired_columns = df[columns] #select specified columns of data
    return list(desired_columns.itertuples(index=False, name=None)) #convert table format into a list where each row is a tuple

def menu_select(options: list[str]) -> int:
    """Print enumerated menu options, prompt user until valid selection, and return the choice"""
    prompt = f"0-{len(options) - 1}:: "
    i = 0
    while i < len(options):
        print(f'[{i}] {options[i]}')
        i += 1

    #user's selection
    selection = int(input(prompt))
    while selection < 0 or selection >= len(options):
        print(f'{selection} is not a valid option\nTry again')
        selection = int(input(prompt))
    return selection


def get_unique_years_from_csv(filename):
    """Add function to parse unique years from CSV for data validation"""
    rows = read_csv_data(filename, ["year"])  
    years = set()
    for row in rows:
        try:
            year = int(row[0])  
            years.add(year)
        except Exception:
            continue
    return sorted(years)
unique_years = get_unique_years_from_csv(DATA_FILE)

def get_unique_source_from_csv(filename):
    """Add skipping empty values check in get_unique_source_from_csv"""
    rows = read_csv_data(filename, ["source"])
    source_set = set()
    for row in rows:
        if row[0]:  #skip null(use if)
            source_set.add(row[0].strip())  
    return sorted(source_set)

unique_source = get_unique_source_from_csv(DATA_FILE)


def print_temperature_for_year_and_source(year_of_interest: int, source: str) -> None:
    """Add function to print temperature for given year and source"""
    data = read_csv_data(DATA_FILE, ["year", "source", "temperature"])
    
    temp_value = None
    for yr, src, temp in data:
        if yr == year_of_interest and src == source:
            temp_value = temp
            break  
    if temp_value is None or temp_value == "NA":
        print(f"No valid temperature record found for source '{source}' in year {year_of_interest}.")
    else:
        print(f"Temperature for source '{source}' in year {year_of_interest}: {temp_value}")

def read_temperature_data(filename: str) -> pd.DataFrame:
    """read file and remove temperature NA"""
    temp_df = pd.read_csv(filename)
    temp_df = temp_df.dropna(subset=['temperature'])
    temp_df['temperature'] = pd.to_numeric(temp_df['temperature'], errors='coerce')
    return temp_df
temp_df = read_temperature_data(DATA_FILE)

def read_anomaly_data(filename: str) -> pd.DataFrame:
    anomaly_df = pd.read_csv(filename)
    anomaly_df = anomaly_df.dropna(subset=['anomaly'])
    anomaly_df['anomaly'] = pd.to_numeric(anomaly_df['anomaly'], errors='coerce')
    return anomaly_df
anomaly_df = read_anomaly_data(DATA_FILE)

def plot_temperature_heatmap(df: pd.DataFrame):
    """Add function to plot heatmap of temperature by year and source"""
    heatmap_data = df.pivot(index='year', columns='source', values='temperature')
    sns.heatmap(heatmap_data)
    plt.title('Temperature Heatmap by Year and Source')
    plt.show()

def plot_anomaly_heatmap(df: pd.DataFrame):
    """Add function to plot heatmap of anomaly by year and source"""
    heatmap_data = df.pivot(index='year', columns='source', values='anomaly')
    sns.heatmap(heatmap_data, cmap="rocket", cbar_kws={"shrink": 0.8})
    plt.title('Anomaly Heatmap by Year and Source', fontsize=16)
    plt.xlabel('source')
    plt.ylabel('year')
    plt.tight_layout()
    plt.show()

def calc_temperature_stats(df: pd.DataFrame):
    """""Add function to calculate mean and standard deviation of temperature grouped by source"""""
    grouped = df.groupby('source')['temperature']
    avg_temp = grouped.mean()
    std_temp = grouped.std()
    max_temp = grouped.max()
    min_temp = grouped.min()
    return avg_temp, std_temp, max_temp, min_temp
avg_temp, std_temp, max_temp, min_temp = calc_temperature_stats(temp_df)

def calc_anomaly_stats(df: pd.DataFrame):
    """Add function to calculate mean, standard deviation,max and min of anomaly grouped by source"""
    grouped = df.groupby('source')['anomaly']
    avg_ano = grouped.mean()
    std_ano = grouped.std()
    max_ano = grouped.max()
    min_ano = grouped.min()
    return avg_ano, std_ano, max_ano, min_ano
avg_ano, std_ano, max_ano, min_ano = calc_anomaly_stats(anomaly_df)

def plot_temperature_boxplot(temp_df):
    """Add temperature boxplot visualization"""
    fig = px.box(temp_df, x='source', y='temperature', title='temperature Distribution by Source')
    fig.show()

def plot_anomaly_boxplot(anomaly_df):
    """Add anomaly boxplot visualization"""
    fig = px.box(anomaly_df, x='source', y='anomaly', title='Anomaly Distribution by Source')
    fig.show()

def main():
    menu_options = [
        "Temperature Report-Single Year",
        "Temperature Over Time Graph",
        "Anomaly Over Time Graph",
        "Summary of Temperature Statistics",
        "Summary of Anomaly Statistics",
        "Temperature Boxplot",
        "Anomaly Boxplot",
        "Exit"
    ]
    option = menu_select(menu_options)
    if option == 0:
        while True:
            try:
                year_input = input(f"Enter a year between {unique_years[0]} and {unique_years[-1]}: ")
                year = int(year_input)
                if year in unique_years:
                    break
                else:
                    print(f"Error: Year {year} not found in the data. Please enter a year from {unique_years[0]} to {unique_years[-1]}.")
            except ValueError:
                print("Error: Invalid year. Please enter a numerical year .")

        while True:
            source = input("Enter a single source name: ").strip()
            if source not in unique_source:
                print(f"Error: The source name '{source}' is not found in the data. Please enter a valid source.")
            else:
                break
        print_temperature_for_year_and_source(year, source)
    elif option == 1:
        plot_temperature_heatmap(temp_df)
    elif option == 2:
        plot_anomaly_heatmap(anomaly_df)
    elif option==3:
        print("Average temperature:")
        print(avg_temp)
        print("\nStandard deviation of temperature:")
        print(std_temp)
        print("\nMax of temperature:")
        print(max_temp)
        print("\nMin deviation of temperature:")
        print(min_temp)
    elif option==4:
        print("Average anomaly:")
        print(avg_ano)
        print("\nStandard deviation of anomaly:")
        print(std_ano)
        print("\nMax of anomaly:")
        print(max_ano)
        print("\nMin deviation of anomaly:")
        print(min_ano)
    elif option==5:
        plot_temperature_boxplot(temp_df)
    elif option==6:
        plot_anomaly_boxplot(anomaly_df)
    elif option==7:
        print("Bye")



main()

