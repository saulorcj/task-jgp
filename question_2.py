"""Answer for question 2 in the JGP task"""

import plotly
import plotly.express as px
import pandas as pd

SERIES_TO_SHOW = "All items, less food and energy"

def get_variation(year: int, df: pd.DataFrame) -> float:
    """Calculate variation in percentage of two prices between two years
    
    - :year: current year
    - :df: df that contains the prices from other years
    - :return: variation of prices
    """

    # if year is the first, do anything
    if year == df['year'].min():
        return None
    
    var = df.loc[df['year'] == year, 'price'].values[0] / df.loc[df['year'] == year - 1, 'price'].values[0] - 1

    return var

def plot_graph(df: pd.DataFrame, series_to_show: str):
    """Show price by month and variation of years
    
    - :df: data series
    - :series_to_show: series name to show
    """

    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year

    # variation over year
    df_var_by_year = df[["year", series_to_show]].groupby("year", as_index=False).mean()

    df_var_by_year.rename(columns={series_to_show: "price"}, inplace=True)

    df_var_by_year['variation'] = df_var_by_year['year'].apply(get_variation, args=[df_var_by_year])

    df_var_by_year['variation'] = df_var_by_year['variation'].apply(lambda x: str(round(x * 100, 2)) + "%" if not pd.isna(x) else None)

    fig = px.line(df, x="date", y=series_to_show, title=f"Price of {series_to_show} by Month & Variation over Years")

    annotations = []

    year_min = 2019
    year_max = 2025

    for _, row in df_var_by_year.iterrows():

        # calculate x position in percentage
        x_position = (row['year'] - year_min) / (year_max - year_min)
        y_position = row['price']

        text = row['variation'] if not pd.isna(row['variation']) else ''

        annotations.append(
            dict(
                xref='paper',
                x=x_position, y=y_position,
                xanchor='center',
                yanchor='middle',
                text=text,
                font=dict(
                    family='Arial',
                    size=16,
                    color='red'
                ),
                showarrow=False
            )
        )

    fig.update_layout(annotations=annotations)

    # set x axes to show all 2024 period
    fig.update_xaxes(range=[pd.to_datetime('2019-01-01'), pd.to_datetime('2025-01-01')], title="Date")
    fig.update_yaxes(title="Price")

    plotly.offline.plot(fig, filename='./exports/graph_q2.html')

    fig.show()

def main():
    """Read CSV file and run plot function"""

    df = pd.read_csv("./exports/pivot_table_series.csv", sep=";", parse_dates=["date"])

    plot_graph(df, SERIES_TO_SHOW)

main()
