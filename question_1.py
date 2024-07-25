"""Answer for question 1 in the JGP task"""

import json

import numpy as np
import pandas as pd
import requests

LINK_API = "https://api.bls.gov/publicAPI/v1/timeseries/data/"

HEADERS = {'Content-type': 'application/json'}

KEY = "7148c6266067497da3daff6cb4f28c25"

NAMES_SERIES_BY_ID = {
    "CUUR0000SA0": "All items",
    "CUUR0000SA0L1E": "All items, less food and energy",
    "CUUR0000SETB01": "Gasoline (all types)"
}

START_YEAR = 2019

END_YEAR = 2024

def get_data_json(list_series: list):
    """Make request to the API and return the series data in json
    
    - :list_series: list of series id
    - :return: series data in json
    """

    data = json.dumps({
        "seriesid": list_series,
        "registrationkey": KEY,
        "startyear": START_YEAR,
        "endyear": END_YEAR
    })

    response = requests.post(LINK_API, headers=HEADERS, data=data, timeout=1000)

    json_data = json.loads(response.text)

    return json_data

def process_data_json(json_data, list_series: list) -> pd.DataFrame:
    """Convert the data to pivot format
    
    - :json_data: json data
    - :list_series: list of series id
    - :return: data in pivot format
    """

    # list of series data in dataframe format
    dfs = []

    for i in range(len(list_series)):
        
        # just to shorten the name
        series_data = json_data['Results']['series'][i]

        # get data
        dfs.append(pd.DataFrame(series_data['data']))

        # get data id
        dfs[i]['nameSeries'] = NAMES_SERIES_BY_ID[series_data['seriesID']]

    # concatenates all dataframe into just one to convert to pivot table
    df = pd.concat(dfs)
    
    df['value'] = df['value'].astype(np.float64)

    df = pd.pivot_table(df,
        values="value",
        index=['year', 'period'],
        columns=['nameSeries'],
        aggfunc='mean'
    ).reset_index(drop=False)

    # create date column
    df['date'] = pd.to_datetime(dfs[0]['period'].apply(lambda month: month[1:]) + '/' + dfs[0]['year'], format='%m/%Y')
    
    df.drop(['year', 'period'], axis=1, inplace=True)

    df = df[['date', 'All items', 'All items, less food and energy', 'Gasoline (all types)']]

    return df

def main() -> None:
    """Main function"""

    series_id = list(NAMES_SERIES_BY_ID.keys())

    json_data = get_data_json(series_id)

    pivot_data = process_data_json(json_data, series_id)

    pivot_data.to_csv("./exports/pivot_table_series.csv", index=False, sep=";")

main()
