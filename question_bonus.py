"""Answer for question bonus in the JGP task"""

from fastapi import FastAPI
import pandas as pd

NAMES_SERIES_BY_ID = {
    "CUUR0000SA0": "All items",
    "CUUR0000SA0L1E": "All items, less food and energy",
    "CUUR0000SETB01": "Gasoline (all types)"
}

app = FastAPI()

@app.get("/series/{series_id}")
def get_series_by_series_id(series_id: str):
    """Get data from a series_id
    
    - :series_id: series_id present in database
    - :return: dict in format {'status': value, 'name': value:, 'data': data}
    """

    if series_id not in NAMES_SERIES_BY_ID:
        return {"status": "Erro", "description": "series_id doesnt exist in database"}

    series_name = NAMES_SERIES_BY_ID[series_id]

    df = pd.read_csv("./exports/pivot_table_series.csv", parse_dates=["date"], sep=";")

    df = df[['date', series_name]].rename(columns={series_name: 'price'})

    return {
        'status': 'ok',
        'name': series_name,
        'data': df.to_dict(orient='records')
    }
