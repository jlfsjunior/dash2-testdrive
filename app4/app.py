import time
from uuid import uuid4
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.long_callback import CeleryLongCallbackManager
from dash.dependencies import Input, Output
from celery import Celery

celery = Celery(
    __name__, 
    broker="redis://localhost:6379/0", 
    backend="redis://localhost:6379/1"
)

launch_uid = uuid4()
print(launch_uid)

long_callback_manager = CeleryLongCallbackManager(
    celery,
    cache_by=[lambda: launch_uid],
    expire=10,
)

app = dash.Dash(
    __name__, 
    long_callback_manager=long_callback_manager,
)

app.layout = html.Div(
    [
        html.Div([html.P(id="paragraph_id", children=["Button not clicked"])]),
        html.Button(id="button_id", children="Run Job!"),
        html.Button(id="cancel_button_id", children="Cancel Running Job!"),
        html.Div(
            [
                dcc.Dropdown(
                    id="country-selection",
                    options=[
                        {"label": "Canada", "value": "CA"},
                        {"label": "United States", "value": "US"},
                        {"label": "Brazil", "value": "BR"},
                    ],
                    value="CA",
                ),
                html.Div(
                    id="output-country",
                ),
            ],
        ),
        html.Div(
            [
                html.H2("Simple callback"),
                dcc.Dropdown(
                    id="country-selection2",
                    options=[
                        {"label": "Canada", "value": "CA"},
                        {"label": "United States", "value": "US"},
                        {"label": "Brazil", "value": "BR"},
                    ],
                    value="CA",
                ),
                html.Div(
                    id="output-country2",
                ),
            ],
        )
    ]
)

@app.callback(
    Output("output-country2", "children"),
    Input("country-selection2", "value"),
)
def update_output2(country):
    print("Should not be cached, right?")
    return "Output for {}".format(country)


@app.long_callback(
    output=Output("output-country", "children"),
    inputs=[Input("country-selection", "value")],
)
def update_output(value):
    print("Second callback running")
    return value

@app.long_callback(
    output=Output("paragraph_id", "children"),
    inputs=Input("button_id", "n_clicks"),
    running=[
        (Output("button_id", "disabled"), True, False),
        (Output("cancel_button_id", "disabled"), False, True),
    ],
    cancel=[Input("cancel_button_id", "n_clicks")],
    prevent_initial_call=True,
)
def callback(n_clicks):
    print("First callback running")
    return "Button clicked"
    time.sleep(2.0)
    return [f"Clicked {n_clicks} times"]


if __name__ == "__main__":
    app.run_server(debug=True)
