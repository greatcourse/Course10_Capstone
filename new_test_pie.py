# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
# print(spacex_df)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

app = dash.Dash(__name__)

# Create layout
app.layout = html.Div([
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id='pie_chart')),
    html.Br(),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 10000: '10000'},
                    value=[min_payload, max_payload]),
    html.Br(),
    html.Div(dcc.Graph(id='payload_scatter_plot'))
])

# Callback for pie chart
@app.callback(Output(component_id='pie_chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value')])
def pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Total Success Launches for Site {entered_site}')
    return fig

# Callback for scatter plot
@app.callback(Output(component_id='payload_scatter_plot', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def payload_scatter_plot(entered_site, payload_slider):
    low, high = payload_slider
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",
                         color='Booster Version Category', 
                         labels={"Payload Mass (kg)": "Payload Mass", 
                                 "class": "Launch Outcome"}, 
                         title="Payload Mass vs. Launch Outcome")
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",
                         color='Booster Version Category', 
                         labels={"Payload Mass (kg)": "Payload Mass", 
                                 "class": "Launch Outcome"}, 
                         title=f"Payload Mass vs. Launch Outcome for {entered_site}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
