from components.aio_component import MarkdownWithColorAIO
# from components.datatable_aio import DataTableAIO
from components.my_aio import SimpleFormAIO

from dash import Dash, html, callback, Input, Output, State
import plotly.express as px

df = px.data.iris()

app = Dash(__name__)

# app.layout = MarkdownWithColorAIO('## Hello World')

# app.layout = MarkdownWithColorAIO(
#     'Custom colors',
#     colors=['cornflowerblue', 'darkolivegreen', 'darkslateblue'],
#     dropdown_props={
#         'persistence': True
#     }
# )

app.layout = html.Div(
    [
        MarkdownWithColorAIO(
            'Custom callback',
            aio_id='color-picker'
        ),
        html.Div(id='color-picker-output'),
        SimpleFormAIO(id="my-aio"),
        # DataTableAIO(df)
    ]
)

@callback(
    Output('color-picker-output', 'children'),
    Input(MarkdownWithColorAIO.ids.dropdown('color-picker'), 'value')
)
def display_color(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)
