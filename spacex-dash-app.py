# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    options = [
                                        {'label': 'All Sites', 'value':'ALL'}]+[
                                        { 'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()
                                    ],
                                    id='site-dropdown',
                                    value='ALL',
                                    placeholder="Select a Launch site here",
                                    searchable=True
                                    ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# add callback decorator
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def get_graph(entered_site):

    if entered_site == 'ALL':
        
        # Contar los lanzamientos exitosos por sitio
        all_data = spacex_df[spacex_df['class'] == 1].groupby(
            'Launch Site'
        ).size().reset_index(name='class')

        # Crear el gráfico circular
        fig = px.pie(
            all_data,
            values='class',
            names='Launch Site',
            title='Successful Launches by Site'
        )

        return fig

    else:

        # Filtrar los datos del sitio seleccionado
        site_data = spacex_df[spacex_df['Launch Site'] == entered_site]

        # Contar lanzamientos exitosos y fallidos
        specific_data = site_data['class'].value_counts().reindex(
            [1, 0], fill_value=0
        ).reset_index()

        specific_data.columns = ['class', 'count']

        # Sustituir los valores numéricos por etiquetas
        specific_data['Outcome'] = specific_data['class'].map({
            1: 'Success',
            0: 'Failure'
        })

        # Crear el gráfico circular
        fig = px.pie(
            specific_data,
            values='count',
            names='Outcome',
            title=f'Outcomes for {entered_site}'
        )

        return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(
        component_id='success-payload-scatter-chart',
        component_property='figure'
    ),
    Input(component_id='payload-slider', component_property='value'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_graph_relation(payload, entered_site):

    if entered_site == 'ALL':

        fig = px.scatter(
            spacex_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload Mass vs. Launch Outcome for All Sites'
        )

        return fig

    else:

        # Filtrar los datos del sitio seleccionado
        site_data = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        fig = px.scatter(
            site_data,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload Mass vs. Launch Outcome for {entered_site}'
        )

        return fig


# Run the app
if __name__ == '__main__':
    app.run()
