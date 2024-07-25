"""Answer for question 4 in the JGP task"""

import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

SERIES_TO_SHOW = "Gasoline (all types)"

def plot_graph(df: pd.DataFrame, series_to_show: str):
    """Show price by month and variation trend per year
    
    - :df: data series
    - :series_to_show: series name to show
    """

    df["year"] = df["date"].dt.year

    df = df[df["year"] >= 2022]

    fig = px.line(df, x="date", y=series_to_show, title=f"Price of {series_to_show} by Month & Variation Trend per Year")

    # set x axes to show all 2024 period
    fig.update_xaxes(range=[pd.to_datetime('2022-01-01'), pd.to_datetime('2025-01-01')], title="Date")
    fig.update_yaxes(title="Price")

    # highlight for period of each year
    fig.add_trace(go.Scatter(
        x=['2022-01-01', '2022-01-01', '2023-01-01', '2023-01-01'],
        y=[180, 160, 160, 180],
        mode="lines",
        name="Decrease 2022"
    ))

    fig.add_trace(go.Scatter(
        x=['2023-01-01', '2023-01-01', '2024-01-01', '2024-01-01'],
        y=[180, 160, 160, 180],
        mode="lines",
        name="Increase 2023"
    ))

    fig.add_trace(go.Scatter(
        x=['2024-01-01', '2024-01-01', '2024-06-01', '2024-06-01'],
        y=[180, 160, 160, 180],
        mode="lines",
        name="Decrease 2024"
    ))

    annotations = []

    year_min = 2022
    year_max = 2025

    # text for period of each year
    for year, text, color in ((2022, 'Price Decrease', 'red'), (2023, 'Price Increase', 'green'), (2024, 'Price Decrease', 'purple')):

        # calculate x position in percentage
        x_position = (year - year_min) / (year_max - year_min)

        if year == 2024:
            x_position += 0.07
        else:
            x_position += 0.166

        y_position = 180

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
                    color=color
                ),
                showarrow=False
            )
        )

    fig.update_layout(annotations=annotations)

    plotly.offline.plot(fig, filename='./exports/graph_q3.html')

    fig.show()

def main():
    """Read CSV file and run plot function"""

    df = pd.read_csv("./exports/pivot_table_series.csv", sep=";", parse_dates=["date"])

    plot_graph(df, SERIES_TO_SHOW)

main()
