# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px



# Create a dash application
app = dash.Dash(__name__)


# Extract unique launch sites
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')
launch_sites = df['Launch Site'].unique()
# Create dropdown options
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}]
for site in launch_sites:
    dropdown_options.append({'label': site, 'value': site})




# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=dropdown_options,
                                    value='ALL',
                                    placeholder='Select a Launch Site',
                                    style={'width': '300px'}),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                        min=0, max=10000, step=1000,
                                        marks={0: '0', 
                                        1000: '1000',
                                        2000: '2000',
                                        3000: '3000',
                                        4000: '4000',
                                        5000: '5000',
                                        6000: '6000',
                                        7000: '7000',
                                        8000: '8000',
                                        9000: '9000',
                                        10000: '10000'

                                        },
                                        value=[df['Payload Mass (kg)'].min(),df['Payload Mass (kg)'].max()]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


# Assuming you have a DataFrame called df containing the data

# Define function to create pie chart for a specific site
@app.callback(
    [Output(component_id='success-pie-chart', component_property='figure'),
     Output(component_id='success-payload-scatter-chart', component_property='figure')],
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_charts(site, payload_value):
    if site == 'ALL':
        filtered_df = df[df['Payload Mass (kg)'].between(payload_value[0], payload_value[1])]
        
        success_launches_by_site = filtered_df.groupby('Launch Site')['class'].sum()
        
        pie_chart = px.pie(
            values=success_launches_by_site.values.tolist(),
            names=success_launches_by_site.index.tolist(),
            title='Total Success by Launch Sites'
        )
        
    else:
        filtered_df = df[
            (df['Payload Mass (kg)'].between(payload_value[0], payload_value[1])) &
            (df['Launch Site'] == site)
        ]
        
        success_rate = filtered_df['class'].mean()
        
        pie_chart = px.pie(
            values=[success_rate, 1 - success_rate],
            names=['Success', 'Failed'],
            title='Success Rate by Chosen Site'
        )

    # TASK 4:
    # Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

    scatter_chart = px.scatter(
        data_frame=filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs. Launch Outcome'
    )

    return pie_chart, scatter_chart







# Run the app
if __name__ == '__main__':
    app.run_server()
