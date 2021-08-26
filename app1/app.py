from components.aio_component import MarkdownWithColorAIO
from dash import Dash, html, callback, Input, Output, State

app = Dash(__name__)

# app.layout = MarkdownWithColorAIO('## Hello World')

# app.layout = MarkdownWithColorAIO(
#     'Custom colors',
#     colors=['cornflowerblue', 'darkolivegreen', 'darkslateblue'],
#     dropdown_props={
#         'persistence': True
#     }
# )

app.layout = html.Div([
    MarkdownWithColorAIO(
        'Custom callback',
        aio_id='color-picker'
    ),
    html.Div(id='color-picker-output')
])

@callback(
    Output('color-picker-output', 'children'),
    Input(MarkdownWithColorAIO.ids.dropdown('color-picker'), 'value')
)
def display_color(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)
