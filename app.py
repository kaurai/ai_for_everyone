from dash import Dash, dash_table, html, dcc
import pandas as pd
import dash_bootstrap_components as dbc

# Load your dataset
data = pd.read_csv("data.csv")  # Replace with your dataset path

# Modify the data to include hyperlinks in the 'ContentType' column and remove the 'link' column
data['ContentType'] = data.apply(lambda row: f"[{row['ContentType']}]({row['link']})", axis=1)
data = data.drop(columns=['link'])  # Drop the 'link' column

# Initialize Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])  # Change theme here

# Expose the Flask server instance for Gunicorn
server = app.server

# App layout
app.layout = dbc.Container(
    [
        # Header with logo, title, and contact button
        dbc.Row(
            dbc.Col(
                dbc.Row([
                    dbc.Col(
                        html.A(
                            html.Img(
                                src="logo.png",  # Path to your logo
                                style={"height": "30px", "margin-right": "1px"}
                            ),
                            href="https://kaurai.com",  # Link to company website
                            target="_blank"
                        ),
                        width="auto"
                    ),
                    dbc.Col(
                        html.H1(
                            "AI.For.Everyone",
                            className="text-primary mb-2",
                            style={"textAlign": "center"}  # Center the title
                        ),
                        width=True  # Ensure the title occupies remaining space
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Contact Us",
                            href="mailto:kaurdotai@gmail.com",
                            color="primary",
                            className="ml-auto",
                            style={"margin-left": "auto", "margin-right": "15px"}
                        ),
                        width="auto"
                    )
                ], align="center", justify="between")  # Adjust alignment to space elements
            )
        ),
        # Dropdown to allow theme switching (optional, for demo purposes)
        dbc.Row(
            dbc.Col(
                html.P(
                    "Ignite a culture of innovation that drives meaningful change.",
                    className="text-muted text-center",
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                html.P(
                    "Disclaimer: Information collected from various internet sources. Please verify the information before making any decisions.",
                    className="text-muted text-center",
                )
            )
        ),
        # Data table
        dbc.Row(
            dbc.Col(
                dash_table.DataTable(
                    id='data-table',
                    columns=[
                        {
                            "name": i, 
                            "id": i,
                            "presentation": "markdown" if i == "ContentType" else None  # Enable markdown for hyperlink column
                        } for i in data.columns
                    ],
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
                        'border': '1px solid #dee2e6',  # Matches table borders
                        'backgroundColor': 'var(--bs-light)',  # Matches the theme's light color
                        'color': 'var(--bs-dark)',  # Matches text color for light themes
                    },
                    style_data_conditional=[
                        {
                            'if': {'state': 'active'},
                            'backgroundColor': 'var(--bs-info)',  # Highlight row on hover
                            'color': 'white',
                        },
                    ],
                    style_cell_conditional=[
                        {
                            'if': {'column_id': 'Description'},
                            'maxWidth': '400px',
                            'whiteSpace': 'normal',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                        {
                            'if': {'column_id': 'ContentType'},
                            'maxWidth': '140px',
                            'whiteSpace': 'normal',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                    ],
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
