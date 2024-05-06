from dash import Dash, html, dcc, Input, Output, callback

from datetime import date

app = Dash(__name__)
app.layout = html.Div([
    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date(2017, 9, 19),
        initial_visible_month=date(2017, 8, 5),
        date=date(2017, 8, 25)
    ),
    html.Div(id='output-container-date-picker-single')
])


@callback(
    Output('output-container-date-picker-single', 'children'),
    Input('my-date-picker-single', 'date'))
def update_output(date_value):
    string_prefix = 'You have selected: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        print(date_object)
        print(date_value)
        return string_prefix + date_string


if __name__ == '__main__':
    app.run(debug=True)
