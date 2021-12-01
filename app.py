import dash
from dash import dash_table
from dash import dcc # dash core components
from dash import html
from dash.dependencies import Input, Output

import pandas as pd

df = pd.read_csv('https://bit.ly/elements-periodic-table')

def identity(x): return x

pt = df.pivot_table(
  index='Period',
  columns='Group', 
  values='Element',
  aggfunc=list,
)

pt_df = pd.DataFrame(pt.to_records())


app = dash.Dash(__name__)

app.layout = html.Div(
  className="main",
  children= [
    html.H2('Test'),
    html.Div(
      className="input-container",
      children=[
        dcc.Dropdown(
          className="dropdown",
          id="index-dropdown",
          options=[{"label": i, "value": i} for i in df.columns],
          multi=False,
          value="Period"),
        dcc.Dropdown(
          className="dropdown",
          id="columns-dropdown",
          options=[{"label": i, "value": i} for i in df.columns],
          multi=False,
          value="Group"),
        dcc.Dropdown(
          className="dropdown",
          id="values-dropdown",
          options=[{"label": i, "value": i} for i in df.columns],
          multi=False,
          value="Element"),
      ]
    ),
    dash_table.DataTable(
      id='table',
      columns=[{"name": i, "id": i} for i in pt_df.columns],
      # columns = [{"name": str(i), "id": str(i)} for i in pt.columns],
      data=pt_df.to_dict('records'),
    )
  ]
)

@app.callback(
  Output(component_id='table', component_property='columns'),
  Output(component_id='table', component_property='data'),
  Input(component_id='index-dropdown', component_property='value'),
  Input(component_id='columns-dropdown', component_property='value'),
  Input(component_id='values-dropdown', component_property='value'),
)
def update_cols(selected_index, selected_columns, selected_values):
  pt = df.pivot_table(
    index=selected_index,
    columns=selected_columns, 
    values=selected_values,
    aggfunc=list,
  )

  pt_df = pd.DataFrame(pt.to_records())
  columns = [{"name": i, "id": i} for i in pt_df.columns]
  data = data=pt_df.to_dict('records')

  return columns, data


app.run_server(debug=True, host="0.0.0.0")