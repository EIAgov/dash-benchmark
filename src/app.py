# -*- coding: utf-8 -*-

from dash import Dash, dcc, html, Input, Output, State, callback, Patch, clientside_callback
import dash_ag_grid as dag
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import dash_bootstrap_components as dbc
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.io as pio
import plotly.graph_objs as go
import numpy as np

from utils.constants import (meta_tags, 
                             find_files, 
                             format_title,  
                             units_dict, 
                             titles_dict, 
                             case_name_labels_dict, 
                             colors_dict,
                             sources_dict)

import gc


work_dir = Path.cwd()

# Uncomment below line out to check your working directory
#print(work_dir)

for path in find_files("eia-aeo-mer-benchmark-nov2024.csv", Path(".")):
    dashboard_data_path = path

    
# we setup the data but use find_files to locate the correct input data file
df = pd.read_csv(dashboard_data_path)

df['edition'] = df['edition'].astype(str)
df = df.iloc[:,1:]


# we standardize the data because of case/scenario labeling in EIA API v2
df['case_name'] = df['case_name'].replace(
    {
        "REF2005": "REFERENCE",
        "REF2006": "REFERENCE",
        "REF2007": "REFERENCE",
        "REF2008": "REFERENCE",
        "REF2009": "REFERENCE", 
        "REF2010R": "REFERENCE",
        "REF2010": "REFERENCE",
        "REF2011": "REFERENCE",
        "REF2012": "REFERENCE",
        "REF2013": "REFERENCE",
        "REF2014": "REFERENCE", 
        "REF2015": "REFERENCE",
        "REF2016": "REFERENCE",
        "REF2017": "REFERENCE",
        "REF2018": "REFERENCE",
        "REF2019": "REFERENCE",
        "REF2020": "REFERENCE",
        "REF2021": "REFERENCE",
        "REF2022": "REFERENCE",
        "REF2023": "REFERENCE",
        "REF2025": "REFERENCE",
        "HM2010": "HIGHMACRO",
        "LM2010": "LOWMACRO",
        "HP2010": "HIGHPRICE",
        "LP2010": "LOWPRICE",
        "HM2011": "HIGHMACRO",
        "LM2011": "LOWMACRO",
        "HP2011HNO": "HIGHPRICE",
        "LP2011LNO": "LOWPRICE", 
        "HEUR12": "HSHLEUR",
        "LEUR12": "LSHLEUR",  
        "HM2012": "HIGHMACRO",
        "LM2012": "LOWMACRO",
        "HP2012": "HIGHPRICE",
        "LP2012": "LOWPRICE", 
        })

df['case_name_labels'] = df['case_name'].map(case_name_labels_dict)


# we focus on certain scenarios or side cases in the review
df = df.loc[df.case_name.isin(['ACTUAL', 'HEUR', 'HIGHMACHIGHZTC', 'HIGHMACLOWZTC', 'HIGHMACRO', 'HIGHOGS', 
                               'HIGHPRICE', 'HIGHRESOURCE', 'HIGHUPIRA', 'HIGHZTC', 'HM2011', 'HM2012', 
                               'LOWMACHIGHZTC', 'LOWMACLOWZTC',
                               'HP2011HNO', 'HP2012', 'HSHLEUR', 'LEUR12', 'LM2011', 'LM2012', 
                               'LOWMACRO', 'LOWOGS', 'LOWPRICE', 'LOWRESOURCE', 'LP2011LNO', 'LP2012', 
                               'LSHLEUR', 'LOWUPIRA', 'LOWZTC', 'NOIRA', 'REFERENCE',
                              ]
                             )
           ]

# sorting helps with later figures
years = np.sort(df.year.unique())
case_names = df.case_name.unique()

# stylesheet with the .dbc class to style dcc, DataTable and AG Grid components with a Bootstrap theme
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"


app = Dash(__name__, meta_tags=meta_tags, 
           title='AEO Retrospective Review', 
           external_stylesheets=[dbc.themes.LUX, dbc.icons.FONT_AWESOME, dbc_css])


color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch(id="switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ]
)

# The ThemeChangerAIO loads all 52  Bootstrap themed figure templates to plotly.io
theme_controls = html.Div(
    [ThemeChangerAIO(aio_id="theme"), color_mode_switch],
    className="hstack gap-3 mt-2"
)

logo = html.Img(src=r'assets/logo_files_forInsideEIAlogopage_bug.svg', width='60px', alt='U.S. Energy Information Administration logo')

header = html.H4("Benchmarking EIA's Annual Energy Outlook: a review of select data series", className="bg-primary text-white p-2 mb-2 text-center"
)


grid = dag.AgGrid(
    id="grid",
    columnDefs=[{"field": i} for i in df.columns],
    rowData=df.to_dict("records"),
    defaultColDef={"flex": 1, "minWidth": 120, "sortable": True, "resizable": True, "filter": True},
    dashGridOptions={"rowSelection":"multiple"}, 
    #csvExportParams= {"filename": "help.csv", "prependContent": "Help"},
)


grid_button = html.Button("Export to csv", id="btn-excel-csv")


dropdown = html.Div(
    [
        dbc.Label("Select indicator (y-axis)"),
        dcc.Dropdown([
            {'label':'imported refiner acquisition cost of crude oil (real 2012$)','value':'PRCE_NA_NA_NA_CR_IMCO_USA_RDLRPBRL'},
            {'label':'imported refiner acquisition cost of crude oil (nominal $)','value':'PRCE_NA_NA_NA_CR_IMCO_USA_NDLRPBRL'},
            {'label':'total petroleum and other liquids consumption','value':'CNSM_NA_LFL_NA_TOT_NA_USA_MILLBRLPDY'},
            {'label':'domestic crude oil production','value':'SUP_PRD_NA_NA_CR_NA_USA_MILLBRLPDY'},
            {'label':'petroleum net imports','value':'TRAD_NA_LFL_TOT_NETIMP_NA_USA_MILLBRLPDY'},
            {'label':'natural gas price (real 2012$), electric power sector','value':'PRCE_DELV_ELEP_NA_NG_NA_USA_RDLRPMCF'},
            {'label':'natural gas price (nominal $), electric power sector','value':'PRCE_DELV_ELEP_NA_NG_NA_USA_NDLRPMCF'},
            {'label':'total natural gas consumption','value':'CNSM_NA_ALLS_NA_NG_TOT_USA_TRLCF'},
            {'label':'dry natural gas production','value':'SUP_DPR_NA_NA_NG_TOT_USA_TRLCF'},
            {'label':'natural gas net imports','value':'TRAD_NETIMP_NA_NA_NG_NA_USA_TRLCF'},
            {'label':'coal prices to electric generating plants (real 2012$)','value':'PRCE_NOM_ELEP_NA_STC_NA_NA_RDLRPMBTU'},
            {'label':'coal prices to electric generating plants (nominal $)','value':'PRCE_NOM_ELEP_NA_STC_NA_NA_NDLRPMBTU'},
            {'label':'total coal consumption','value':'CNSM_NA_NA_NA_CL_NA_NA_MILLTON'},
            {'label':'coal production excluding waste coal','value':'SUP_NA_NA_NA_CL_NA_NA_MILLTON'},
            {'label':'average electricity prices (real 2012$)','value':'PRCE_NA_ELEP_NA_EDU_NA_USA_RCNTPKWH'},
            {'label':'average electricity prices (nominal $)','value':'PRCE_NA_ELEP_NA_EDU_NA_USA_NCNTPKWH'},
            {'label':'total electricity sales excluding direct use','value':'CNSM_NA_ELEP_NA_ELS_NA_USA_BLNKWH'},
            {'label':'solar net generation (all sectors)','value':'GEN_NA_ALLS_NA_SLR_NA_NA_BLNKWH'},
            {'label':'wind net generation (all sectors)','value':'GEN_NA_ALLS_NA_WND_NA_NA_BLNKWH'},
            {'label':'conventional hydroelectric power net generation (all sectors)','value':'GEN_NA_ELEP_NA_HYD_CNV_NA_BLNKWH'},
            {'label':'coal net generation (all sectors)','value':'GEN_NA_ELEP_TGE_CL_NA_USA_BLNKWH'},
            {'label':'natural gas net generation (all sectors)','value':'GEN_NA_ELEP_TGE_NG_NA_USA_BLNKWH'},
            {'label':'nuclear net generation (all sectors)','value':'GEN_NA_ELEP_TGE_NUP_NA_USA_BLNKWH'},
            {'label':'total energy consumption (all sectors)','value':'CNSM_ENU_TEN_NA_TOT_NA_NA_QBTU'},
            {'label':'total delivered residential energy consumption','value':'CNSM_ENU_RES_NA_DELE_NA_NA_QBTU'},
            {'label':'total delivered commercial energy consumption','value':'CNSM_ENU_COMM_NA_DELE_NA_NA_QBTU'},
            {'label':'total delivered industrial energy consumption','value':'CNSM_ENU_IDAL_NA_DELE_NA_NA_QBTU'},
            {'label':'total delivered transportation energy consumption','value':'CNSM_ENU_TRN_NA_DELE_NA_NA_QBTU'},
            {'label':'total energy-related carbon dioxide emissions','value':'EMI_CO2_NA_NA_NA_NA_NA_MILLMTCO2EQ'},
            {'label':'energy intensity','value':'INY_NA_NA_NA_TEN_NA_NA_THBTUPDLRGDP'}],
            "PRCE_NA_NA_NA_CR_IMCO_USA_RDLRPBRL",
            id="indicator",
            clearable=False,
        ),
    ],
    className="mb-4",
)


checklist = html.Div(
    [
        dbc.Label("Select AEO Case or MER Actual"),
        dcc.Dropdown([
            {'label':'Actual','value':'ACTUAL'},
            {'label':'Oil and Gas: High Shale EUR','value':'HSHLEUR'},
            {'label':'High Macro and High Zero-Carbon Technology Cost','value':'HIGHMACHIGHZTC'},
            {'label':'High Macro and Low Zero-Carbon Technology Cost','value':'HIGHMACLOWZTC'},
            {'label':'High Economic Growth','value':'HIGHMACRO'},
            {'label':'High Oil and Gas Supply','value':'HIGHOGS'},
            {'label':'High Oil Price','value':'HIGHPRICE'},
            {'label':'Oil and Gas: High Oil and Gas Resource','value':'HIGHRESOURCE'},
            {'label':'High Uptake of Inflation Reduction Act','value':'HIGHUPIRA'},
            {'label':'High Zero-Carbon Technology Cost','value':'HIGHZTC'},
            {'label':'Low Macro and High Zero-Carbon Technology Cost','value':'LOWMACHIGHZTC'},
            {'label':'Low Macro and Low Zero-Carbon Technology Cost','value':'LOWMACLOWZTC'}, 
            {'label':'Oil and Gas: Low Shale EUR','value':'LSHLEUR'},
            {'label':'Low Economic Growth','value':'LOWMACRO'},
            {'label':'Low Oil and Gas Supply','value':'LOWOGS'},
            {'label':'Oil and Gas: Low Oil and Gas Resource','value':'LOWRESOURCE'},
            {'label':'Low Oil Price','value':'LOWPRICE'},
            {'label':'Low Uptake of Inflation Reduction Act','value':'LOWUPIRA'},
            {'label':'Low Zero-Carbon Technology Cost','value':'LOWZTC'},
            {'label':'No Inflation Reduction Act','value':'NOIRA'},
            {'label':'Reference case','value':'REFERENCE'}],
            case_names, 
            id="case_names", 
            clearable=False, 
            multi=True,
        )
    ], 
    className="mb-4",
)

slider = html.Div(
    [
        dbc.Label("Select Years"),
        dcc.RangeSlider(
            years[0],
            years[-1],
            1,
            id="years",
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            value=[years[21], years[-1]],
            className="p-0",
        ),
    ],
    className="mb-4",
)


theme_colors = [
    "primary",
    "secondary",
    "success",
    "warning",
    "danger",
    "info",
    "light",
    "dark",
    "link",
]


colors = html.Div(
    [dbc.Button(f"{color}", color=f"{color}", size="sm") for color in theme_colors]
)


colors = html.Div(["Theme Colors:", colors], className="mt-2")
colors = html.Div(f" ")


controls = dbc.Card(
    [dropdown, checklist, slider], 
    body=True,
)
citation_controls = html.Div(
    [], id="fig-citation", className="mt-2")
citation_controls = html.Div([citation_controls, html.A("Link to EIA's open data API for Annual Energy Outlooks ", href='https://www.eia.gov/opendata/browser/aeo', target="_blank"), 
                              html.Div([html.A("Link to EIA's open data API for Monthly Energy Reviews", href='https://www.eia.gov/opendata/browser/total-energy', target="_blank")]), 
                              ])
"""
citations  = dbc.Card(
    [citation], 
    body=True,
)
"""


tab1 = dbc.Tab([dcc.Graph(id="line-chart", figure=px.line(template="simple_white"), style={'height': '85vh'})], label="Line Chart")
tab2 = dbc.Tab([dcc.Graph(id="scatter-chart", figure=px.scatter(template="simple_white"), style={'height': '85vh'})], label=" ", disabled=True)
tab3 = dbc.Tab([grid,grid_button], label="Grid", className="p-4")
tabs = dbc.Card(dbc.Tabs([tab1, tab3, tab2]))


app.layout = dbc.Container(
    [
        header,
        dbc.Row([
            dbc.Col([
                controls,
                # ************************************
                # Uncomment line below when running locally!
                # ************************************
                theme_controls
            ],  width=3),
            dbc.Col([tabs, citation_controls], width=9),
        ]),
    ],
    fluid=True,
    #style={"height": "100vh"},
    className="dbc dbc-ag-grid",
)


@callback(
    Output("line-chart", "figure" ),
    Output("scatter-chart", "figure"),
    Output("grid", "dashGridOptions"),
    Output("fig-citation", component_property='children'),
    Input("indicator", "value"),
    Input("case_names", "value"),
    Input("years", "value"),
    State(ThemeChangerAIO.ids.radio("theme"), "value"),
    State("switch", "value"),
)
def update(indicator, case_name, yrs, theme, color_mode_switch_on):

    # Defining all the conditions inside a function
    def conditions_(x):
        if x=="2024":
            return fig.update_traces(line_color='purple')
        elif x=="2021":
            return fig.update_traces(line_color='green')
        else:
            return None
        
    def conditions_prefix(x):
        if x=="PRCE":
            return fig.update_layout(yaxis=dict(tickprefix= '$', separatethousands= True, tickfont_size=26))
        else:
            return None


    if case_name == [] or indicator is None:
        return {}, {}, {}

    theme_name = template_from_url(theme)
    template_name = theme_name if color_mode_switch_on else theme_name + "_dark"

    dff = df[df.year.between(yrs[0], yrs[1])]
    dff = dff[dff.case_name.isin(case_name)]
    dff['PER_CAPITA'] = dff[indicator].div(dff['DMG_POP_NA_NA_NA_NA_NA_MILL'])
    dff['GDP_PER_CAPITA'] = (dff["ECI_NA_NA_NA_GDP_REAL_NA_BLNY09DLR"].div(dff['DMG_POP_NA_NA_NA_NA_NA_MILL'])).mul(1000)
    test_units = indicator.rsplit('_',1)[-1]
     
    fig = px.line(
        dff.sort_values(by=["edition","case_name_labels"],ascending=True),
        x="year",
        y=indicator,
        color="edition",
        line_group="case_name_labels",
        #line_dash="case_name",
        labels={"edition": "edition", "case_name_labels": "case"},
        title=f"<b>{titles_dict.get(indicator,'title not found')}</b><br>({units_dict.get(test_units,'units not found')})",
        template=template_name,
    )

    fig.for_each_trace(
        lambda trace: trace.update(line_color="black", line_width=4) if trace.legendgroup == "2024" else (),)
    
    fig.update_layout(yaxis=dict(title=None, tickfont_size=26), 
                      xaxis=dict(tickfont_size=26, automargin=True),
                      legend=dict(font=dict(size=26,)), title=dict(font=dict(size=26)),  
                      paper_bgcolor='rgba(0, 0, 0, 0)',
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      modebar=dict(
                        orientation='h',
                        bgcolor='#ffffff',
                        color='red',
                        activecolor='red',
                        )
                        )
    

    conditions_prefix(indicator[:4])

    fig.update_xaxes(
        mirror=False,
        ticks='outside',
        showline=True,
        linecolor='black',
        linewidth=2, 
        gridcolor='lightgrey',
        title_font = {"size": 26},
        title_standoff = 1,
        range=(2000, 2050)
    )
    fig.update_yaxes(
        mirror=True,
        ticks=None,
        showline=False,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.update_traces(selector=dict(legendgroup="2005"), line=dict(color=colors_dict.get('dhs-dark-gray-70')))
    fig.update_traces(selector=dict(legendgroup="2006"), line=dict(color=colors_dict.get('dhs-dark-gray-60')))
    fig.update_traces(selector=dict(legendgroup="2007"), line=dict(color=colors_dict.get('dhs-dark-gray-40')))
    fig.update_traces(selector=dict(legendgroup="2008"), line=dict(color=colors_dict.get('dhs-dark-gray-30')))
    fig.update_traces(selector=dict(legendgroup="2009"), line=dict(color=colors_dict.get('dhs-dark-gray-20')))
    fig.update_traces(selector=dict(legendgroup="2010"), line=dict(color=colors_dict.get('dhs-green-70')))

    fig.update_traces(selector=dict(legendgroup="2011"), line=dict(color=colors_dict.get('dhs-green-60')))
    fig.update_traces(selector=dict(legendgroup="2012"), line=dict(color=colors_dict.get('dhs-green-40')))
    fig.update_traces(selector=dict(legendgroup="2013"), line=dict(color=colors_dict.get('dhs-green-30')))
    fig.update_traces(selector=dict(legendgroup="2014"), line=dict(color=colors_dict.get('dhs-green-20')))

    fig.update_traces(selector=dict(legendgroup="2015"), line=dict(color=colors_dict.get('dhs-red-70')))
    fig.update_traces(selector=dict(legendgroup="2016"), line=dict(color=colors_dict.get('dhs-red-60')))
    fig.update_traces(selector=dict(legendgroup="2017"), line=dict(color=colors_dict.get('dhs-red-40')))
    fig.update_traces(selector=dict(legendgroup="2018"), line=dict(color=colors_dict.get('dhs-red-30')))
    fig.update_traces(selector=dict(legendgroup="2019"), line=dict(color=colors_dict.get('dhs-red-20')))
    fig.update_traces(selector=dict(legendgroup="2020"), line=dict(color=colors_dict.get('dhs-light-blue-70')))
    fig.update_traces(selector=dict(legendgroup="2021"), line=dict(color=colors_dict.get('dhs-light-blue-60')))
    fig.update_traces(selector=dict(legendgroup="2022"), line=dict(color=colors_dict.get('dhs-light-blue-40')))
    fig.update_traces(selector=dict(legendgroup="2023"), line=dict(color=colors_dict.get('dhs-light-blue-30')))
    

    textString = f"{sources_dict.get(indicator,'not found')}. Note: Dollars are adjusted to 2012$, unless noted otherwise."
    
    # Add the annotation text using paper reference. See:
    # https://stackoverflow.com/questions/76046269/how-to-align-annotation-to-the-edge-of-whole-figure-in-plotly
    # https://community.plotly.com/t/interactive-app-to-explain-legend-and-annotations-positioning/65160
    """
    fig.add_annotation(
        text = textString,
        font = {
            'size' : 14,
            'color': 'gray',
        },
        xref = "paper", 
        yref = "paper",
        x = -0.01, 
        y = -0.09, #yCord - yOffset,
        align='left',        
        showarrow = False
    )
    """

        
    fig_scatter = px.scatter(
        dff[(dff.edition >= "2023")].sort_values(by=["year","edition"]),
        x="GDP_PER_CAPITA",
        y=indicator,
        color="case_name_labels",
        color_discrete_map={
            'High Macro and High Zero-Carbon Technology Cost': "#3182bd",
            'High Macro and Low Zero-Carbon Technology Cost': "#31a354",
            'High Economic Growth': "#e6550d",
            'High Oil and Gas Supply': "#756bb1",
            'High Oil Price': "#de2d26",
            'High Uptake of Inflation Reduction Act': "#6e40aa",
            'High Zero-Carbon Technology Cost': "#80cdc1",
            'Low Macro and High Zero-Carbon Technology Cost': "#9ecae1",
            'Low Macro and Low Zero-Carbon Technology Cost': "#a1d99b",
            'Low Economic Growth': "#fdae6b",
            'Low Oil and Gas Supply': "#bcbddc",
            'Low Oil Price': "#fc9272",
            'Low Uptake of Inflation Reduction Act': "#aff05b",
            'Low Zero-Carbon Technology Cost': "#28ea8d",
            'No Inflation Reduction Act': "#a6611a",
            'Reference case': "#dfc27d",
            'Actual': "black",
            },
        symbol="edition",
        log_x=True,
        labels={indicator: f"{titles_dict.get(indicator,'title not found')} ", "GDP_PER_CAPITA": "real GDP per capita", "edition": "edition", "case_name_labels": "case"},
        size_max=60,
        template=template_name,
        title=f"<b>{titles_dict.get(indicator,'title not found')} vs. Real GDP per capita</b><br>({units_dict.get(test_units,'units not found')})", 
        )


    fig_scatter.update_traces(textposition="bottom right")
    fig_scatter.update_layout(yaxis=dict(title=None, exponentformat= None, separatethousands= True, tickfont_size=26), 
                              xaxis=dict(tickprefix= '$', separatethousands= True, tickfont_size=26) )
    fig_scatter.for_each_trace(
        lambda trace: trace.update(marker=dict(size=10, color="black"), line=dict(width=2, color="DarkSlateGrey")) if trace.name == "Actual, 2024" else 
        (trace.update(marker=dict(size=8), line=dict(width=2, color="DarkSlateGrey"))),)
    fig_scatter.update_xaxes(showline=True, linewidth=2, linecolor='black')


    # Add the annotation text using paper reference. See:
    # https://stackoverflow.com/questions/76046269/how-to-align-annotation-to-the-edge-of-whole-figure-in-plotly
    # https://community.plotly.com/t/interactive-app-to-explain-legend-and-annotations-positioning/65160
    fig_scatter.add_annotation(
        text = textString,
        font = {
            'size' : 14,
            #'family' : 'Times New Roman',
            'color': 'gray',
        },
        xref = "paper", 
        yref = "paper",
        x = -0.01, 
        y = -0.15,  
        align='left',
        showarrow = False
    )


    grid_filter = f"{case_name}.includes(params.data.case_name) && params.data.year >= {yrs[0]} && params.data.year <= {yrs[1]}"
    dashGridOptions = {
        "isExternalFilterPresent": {"function": "true"},
        "doesExternalFilterPass": {"function": grid_filter},
    }
    fig_scatter.update_traces(visible='legendonly', selector=dict(name="d")) 

    return fig, fig_scatter, dashGridOptions, textString


# updates the Bootstrap global light/dark color mode
clientside_callback(
    """
    switchOn => {       
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """,
    Output("switch", "id"),
    Input("switch", "value"),
)

clientside_callback(
    """function (n) {
        if (n) {
            dash_ag_grid.getApi("grid").exportDataAsCsv();
        }
        return dash_clientside.no_update
    }""",
    Output("btn-excel-csv", "n_clicks"),
    Input("btn-excel-csv", "n_clicks"),
    prevent_initial_call=True
)


# This callback makes updating figures with the new theme much faster
@callback(
    Output("line-chart", "figure", allow_duplicate=True ),
    Output("scatter-chart", "figure", allow_duplicate=True),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    Input("switch", "value"),
    prevent_initial_call=True
)
def update_template(theme, color_mode_switch_on):
    theme_name = template_from_url(theme)
    template_name = theme_name if color_mode_switch_on else theme_name + "_dark"

    patched_figure = Patch()
    # When using Patch() to update the figure template, you must use the figure template dict
    # from plotly.io  and not just the template name
    patched_figure["layout"]["template"] = pio.templates[template_name]
    return patched_figure, patched_figure


if __name__ == "__main__":
    app.run_server(debug=True)