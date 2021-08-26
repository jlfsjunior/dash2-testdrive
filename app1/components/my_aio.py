from dash import Dash, Output, Input, State, html, dcc, callback, MATCH
import uuid

class SimpleFormAIO(html.Div):

    class ids:
        name_input = lambda aio_id: {
            'component': 'SimpleFormAIO',
            'subcomponent': 'name_input',
            'aio_id': aio_id
        }
        country_input = lambda aio_id: {
            'component': 'SimpleFormAIO',
            'subcomponent': 'country_input',
            'aio_id': aio_id
        }
        submit_button = lambda aio_id: {
            'component': 'SimpleFormAIO',
            'subcomponent': 'submit_button',
            'aio_id': aio_id
        }
        output_div = lambda aio_id: {
            'component': 'SimpleFormAIO',
            'subcomponent': 'output_div',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(
        self,
        aio_id=None,
        name_placeholder='Name',
        country_placeholder='Country',
        submit_button_text='Submit',
        submit_button_style={'color': '#ffffff', 'background-color': '#0074d9'},
        submit_button_class='btn btn-primary',
        submit_button_callback=None,
        **kwargs
    ):
        
        self.aio_id = aio_id or str(uuid.uuid4())
        self.name_placeholder = name_placeholder
        self.country_placeholder = country_placeholder
        self.submit_button_text = submit_button_text
        self.submit_button_style = submit_button_style
        self.submit_button_class = submit_button_class
        self.submit_button_callback = submit_button_callback

        return super().__init__([
            html.Div(
                [
                    dcc.Input(id=self.ids.name_input(self.aio_id), placeholder=self.name_placeholder),
                    dcc.Input(id=self.ids.country_input(self.aio_id), placeholder=self.country_placeholder),
                ]
            ),
            html.Button(
                id=self.ids.submit_button(self.aio_id), 
                children=self.submit_button_text, 
                style=self.submit_button_style, 
                className=self.submit_button_class
            ),
            html.Div(id=self.ids.output_div(self.aio_id)),
        ])

    @callback(
        output=Output(ids.output_div(MATCH), 'children'),
        inputs=Input(ids.submit_button(MATCH), 'n_clicks'),
        state=[
            State(ids.name_input(MATCH), 'value'), 
            State(ids.country_input(MATCH), 'value')
        ],
    )
    def submit_form(n_clicks, name, country):
        if n_clicks is not None and n_clicks > 0:
            return 'Hello {} from {}'.format(name, country)
        else:
            return ''
    