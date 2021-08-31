import time
from uuid import uuid4
import dash
from dash import html
from dash.long_callback import DiskcacheLongCallbackManager
from dash.dependencies import Input, Output

## Diskcache
import diskcache

launch_uid = uuid4()
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(
    cache, 
    cache_by=[lambda: launch_uid], 
    expire=60,
)

app = dash.Dash(__name__, long_callback_manager=long_callback_manager)

app.layout = html.Div(
    [
        html.Div([html.P(id="paragraph_id", children=["Button not clicked"])]),
        html.Button(id="button_id", children="Run Job!"),
        html.Button(id="cancel_button_id", children="Cancel Running Job!"),
    ]
)


@app.long_callback(
    output=(Output("paragraph_id", "children"), Output("button_id", "n_clicks")),
    inputs=Input("button_id", "n_clicks"),
    running=[
        (Output("button_id", "disabled"), True, False),
        (Output("cancel_button_id", "disabled"), False, True),
    ],
    cancel=[Input("cancel_button_id", "n_clicks")],
    prevent_initial_call=True,
)
def callback(n_clicks):

    print("This won't run for n_clicks < cached value")

    time.sleep(2.0)
    return [f"Clicked {n_clicks} times"], (n_clicks or 0) % 4


if __name__ == "__main__":
    app.run_server(debug=True)