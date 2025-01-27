from dash import Dash, dash_table, html, dcc
import pandas as pd
import dash_bootstrap_components as dbc

# Load your dataset
data = pd.read_csv("currency.csv")  # Replace with your dataset path

# Initialize Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])  # Change theme here

# App layout
app.layout = dbc.Container(
    [
        # Header
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Interactive Data Table",
                    className="text-center text-primary mb-4",
                )
            )
        ),
        # Dropdown to allow theme switching (optional, for demo purposes)
        dbc.Row(
            dbc.Col(
                html.P(
                    "This table integrates seamlessly with the Bootstrap theme you select.",
                    className="text-muted text-center",
                )
            )
        ),
        # Data table
        dbc.Row(
            dbc.Col(
                dash_table.DataTable(
                    id='data-table',
                    columns=[{"name": i, "id": i} for i in data.columns],
                    data=data.to_dict('records'),
                    filter_action="native",  # Add filtering
                    sort_action="native",    # Add sorting
                    page_size=50,            # Paginate 10 rows
                    style_table={'overflowX': 'auto'},  # Enable horizontal scrolling
                    style_cell={
                        'padding': '10px',
                        'fontFamily': 'Arial, sans-serif',
                        'fontSize': '16px',
                        'textAlign': 'left',
                        'border': '1px solid #dee2e6',  # Matches table borders in Bootstrap
                    },
                    style_header={
                        'backgroundColor': 'var(--bs-primary)',  # Use Bootstrap's primary color
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textAlign': 'center',
                        'border': '1px solid #dee2e6',
                    },
                    style_data={
                        'border': '1px solid #dee2e6',  # Matches Bootstrap table borders
                        'backgroundColor': 'var(--bs-light)',  # Matches the theme's light color
                        'color': 'var(--bs-dark)',  # Matches text color for light themes
                    },
                    style_data_conditional=[
                        # {
                        #     'if': {'row_index': 'odd'},
                        #     'backgroundColor': 'var(--bs-body-bg)',  # Alternate row colors
                        # },
                        {
                            'if': {'state': 'active'},
                            'backgroundColor': 'var(--bs-info)',  # Highlight row on hover
                            'color': 'white',
                        },
                    ],
                )
            )
        ),
        # Footer
        dbc.Row(
            dbc.Col(
                html.Footer(
                    html.A(
                        "Contact Kaur.AI",  # Replace with your email
                        href="mailto:kaurdotai@gmail.com",  # Hyperlink to send an email
                        className="text-center text-muted",
                        style={"textDecoration": "none", "color": "inherit"}  # Ensures no underline and matches theme color
                    ),
                    className="text-center mt-4",
                )
            )
        ),
    ],
    fluid=True,
    style={"padding": "20px"},
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
