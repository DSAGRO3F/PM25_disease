
import dash
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
#import plotly.graph_objects as go
import os



"""layout design"""
dash.register_page(__name__,
                   path='/',
                   title='db-stroke',
                   name='db-stroke',
                   location="sidebar")



"""build dictionary to help understanding of main vocabulory"""
d_vocab = {
    'GBD': 'global burden desease',
    'CRF': 'concentration response function',
    'PM2.5': 'Fine particulate matter is defined as particles that are 2.5 microns or less in diameter',
    'IHD': 'ischemic heart disease',
    'Stroke': 'stroke',
    'COPD': 'chronic obstructive pulmonary disease',
    'LC': 'lung cancer',
    'LRI': 'lower respiratory infections',
    'DM': 'type II diabetes',
    'LBW': 'low birth weight',
    'PTB': 'pre-term births'}



"""from dict, build df"""
def build_df(d):
    list_keys = list(d.keys())
    #print(f'keys: {list_keys}')
    list_values = [d[key] for key in list_keys]
    df = pd.DataFrame(list_keys, columns=['acronyms'], index=range(len(d)))
    df['acronym_meaning'] = list_values
    #print(f'{df}')
    return df
df = build_df(d_vocab)



"""load df's"""
path = '/Users/olivierdebeyssac/Python_pollution_analysis/data/GBD2019'

def load_dfs(path):
    l_df = []
    l_words = []
    l_years = []
    
    list_files = [file for file in os.listdir(path) if file.endswith('.csv')]
    l_1 = [file for file in list_files if 'Lower' not in file]
    l_2 = [file for file in l_1 if 'Upper' not in file]
    l_3 = [file for file in l_2 if 'GEMM' not in file]
    l_4 = [file for file in l_3 if 'MRBRT' not in file]
    
    nb_elements = len(l_4)
    #print(f'nb_elements dans l_4 : {nb_elements}')
    #print(f'l_4 : {l_4}')
    
    #restricted_words_list = ['COPD', 'DM', 'IHD', 'LBW', 'LC', 'LRI', 'PTB', 'Stroke']
    
    for file in l_4:
        idx = l_4.index(file)
        if idx < nb_elements:
            words_in_name_file = file.split('_')
            if words_in_name_file[0] != 'CoExposure':
                year = file.split('_')[-4]
                word = file.split('_')[-1].split('.')[-2]
            
                l_years.append(year)
                l_words.append(word)
            
                df = pd.read_csv(path+'/'+file)
                l_df.append(df)
                
            else:
                df = pd.read_csv(path+'/'+file)
                df_iso = df.loc[:, ['Location', 'ISO3']]
    
    return l_years, l_words, l_df, df_iso

l_years, l_words, l_df, df_iso = load_dfs(path)
list_of_d_words = [{str(word): word} for word in l_words]
list_of_d_years = [{str(year): year} for year in l_years]

# Prints
# print(f'l_years : {l_years}, nb_years: {len(l_years)}')
# print(f'l_words : {l_words}, nb_words: {len(l_words)}')
# print(f'l_df[0] --- {l_df[0]}')
# print(f'df_iso: {df_iso.head()}')
# print(f'list_of_d_years : {list_of_d_years}')




"""Build dictionary of words and their related index"""
d_word_idx = [{"word": word, "year": year, "index": i} for i, (word, year) in enumerate(zip(l_words, l_years))]
#print(f'd_word_idx: {d_word_idx}')




"""add 'iso' feature to loaded dataframes for building graphs"""
def add_iso_feature(l):
    new_list = []
    for df in l:
        df_merged = df.merge(df_iso, how='left', on='Location')
        #df_merged.set_index('Location', drop=True, inplace=True)
        new_list.append(df_merged)


    #Prints
    #print(f'Second df merged: {new_list[1].head()}')
    #print(f'len(new_list): {len(new_list)}')
    
    return new_list
        
new_list = add_iso_feature(l_df) # new_list contains df with added feature 'iso'

# Prints
#print(f'new_list[0].head() --- {new_list[0].iloc[0:5, 0:5]}')
#print(f'new_list[1].head() --- {new_list[1].iloc[0:5, 0:5]}')

#print(f'new_list[0].index: {list(new_list[0].index)}')
#print(f'new_list[0].to_dict: {new_list[0].to_dict("records")}')




"""build country dictionnary {label, value} expected by dropdown component options"""
list_of_dictionaries = [{"label": str(country), "value": country} for country in new_list[0].loc[:, 'Location']]

# Prints
# print(f'list_of_dictionaries: {list_of_dictionaries}')
# print(f'nb of dict: {len(list_of_dictionaries)}')



"""create list of dictionnaries of n items each"""
def create_list_of_dict(l, n):
    
    # print(f'len(l): {len(l)}')
    
    l_idx = []
    l_of_d = []
    l_of_lists = []
    
    for i in range(len(l)):
        l_idx.append(i)
        nb_elements = len(l_idx)
        # print(f'nb_elements: {nb_elements}')
        
        if nb_elements <= n:
            l_of_d.append(l[i])
            
        if nb_elements > n:
            l_of_lists.append(l_of_d)
            l_idx = []
            l_of_d = []
    return l_of_lists
        
l_of_lists = create_list_of_dict(list_of_dictionaries, 12)

#Prints
#print(f'l_of_lists: {l_of_lists}')
#print()
#print(f'nb of elements in dictionnaries: {len(l_of_lists)}')
#print(f'len(l_of_lists): {len(l_of_lists[0])}')






"""layout"""
layout = dbc.Container([
    
    html.Div(
        [dcc.Store(id=f'store-{i}', data=new_list[i].to_dict('records')) for i in range(len(new_list))
        ]
        ),
    html.Div([dcc.Store(id='store-list_dict', data=l_of_lists)]),
    html.Div([dcc.Store(id='store-words', data=list_of_d_words)]),
    html.Div([dcc.Store(id='store-years', data=list_of_d_years)]),
    
    #html.Div(id='words-output', children=[]),

    dbc.Row([
        html.H1('Information on datasets', style={'textAlign': 'center'}),
        html.Br(),
        html.Br(),
        dcc.Markdown('''
                      **Source sector & fuel contribution to ambient PM 2.5**
                     
                     
                      [https://dash.plotly.com/dash-core-components/markdown/1000]/
                     
                     
                      '''),
                      ]),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(id='table-description', data=df.to_dict('records'),
                                  columns=[{"name": col, "id": col} for col in df.columns],
                                  page_size=15,
                                  fixed_columns={'headers': True, 'data': 1},
                                  style_cell={'textAlign': 'left', 'padding': '5px'},
                                  style_header={'backgroundColor': 'white','fontWeight': 'bold', 'border': '1px solid pink'},
                                  style_data={ 'border': '1px solid blue' }),
            ]),
        
        dbc.Col([
            dcc.Markdown('''
                          The global ambient PM2.5 disease burden was estimated by integrating national-level annual PWM PM2.5 concentrations with CRFs49 and national baseline data consistent with the 2019 GBD1 (GBD2019 CRF). 
                          These updated CRFs better reflect the uncertainty of health effects at high PM2.5 concentrations. 
                         
                          Globally, we estimate that **3.83 million deaths*** (95% Confidence Interval: 2.72–4.97 million) were attributable to annual ambient PM2.5 exposure in the year 2017. 
                        
                          Attributable deaths were primarily from **ischemic heart disease (IHD) and Stroke**, followed by **chronic obstructive pulmonary disease (COPD)**, **lung cancer (LC)**, **lower respiratory infections (LRI)**, and **type II diabetes (DM)**. 
                        
                          In addition, there were a **total of 2.07 million** attributable incidences of **neonatal disorders, low birth weight (LBW)** and **pre-term births (PTB)**, worldwide.
                        
                          The **largest numbers of attributable deaths occurred in China (~1.4 million)** and **India (0.87 million)**, together accounting for 58% of the global total ambient PM2.5 mortality burden. 
                        
                          The larger burden in China, despite a lower national PM2.5 exposure level reflects differences in population age distribution and the relative baselines associated with each disease in each country. 
                        '''),
                ]),
            ]),
                         
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Hr(),
            html.Br(),
            ])
        ]),
            
    dbc.Row([
        dbc.Col([
            html.H2(f'Data table -- {l_words[0]} -- {l_years[0]}'),
            dash_table.DataTable(id='full-table-2017',
                                  data=[],
                                  page_size=15,
                                  fixed_columns={'headers': True, 'data': 1},
                                  style_cell={'padding': '5px'},
                                  style_header={'backgroundColor': 'white','fontWeight': 'bold', 'border': '1px solid pink'},
                                  style_data={ 'border': '1px solid blue' })]),
                
        dbc.Col([
            html.H2(f'Graph -- {l_words[0]} -- {l_years[0]}'),
            dcc.Graph(id='all-countries-2017', figure={})
            ])
        ]),
    
    dbc.Row([
        dbc.Col([
            html.H2(f'Data table -- {l_words[4]} -- {l_years[4]}'),
            dash_table.DataTable(id='full-table-2019',
                                  data=[],
                                  page_size=15,
                                  fixed_columns={'headers': True, 'data': 1},
                                  style_cell={'padding': '5px'},
                                  style_header={'backgroundColor': 'white','fontWeight': 'bold', 'border': '1px solid pink'},
                                  style_data={ 'border': '1px solid blue' })]),
        
        dbc.Col([
            html.H2(f'Graph -- {l_words[4]} -- {l_years[4]}'),
            dcc.Graph(id='all-countries-2019', figure={})
            ])
        ]),
        
    html.Br(),
    html.Hr(),
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Markdown(f'''# **Most affected countries, {l_words[0]}, {l_years[0]}:**'''),
                dcc.Markdown(id='markdown-top-3-countries-2017'),
                ]),
            
            html.Br(),
            
            html.Div([
                dcc.Markdown(f'''# **Most affected countries, Totals, {l_words[0]}, {l_years[0]}:**'''),
                dcc.Markdown(id='markdown-top-3-total-2017')
                ]),
            ]),
        
        dbc.Col([
            html.Div([
                dcc.Markdown(f'''# **Most affected countries, {l_words[4]}, {l_years[4]}, Total:**'''),
                dcc.Markdown(id='markdown-top-3-countries-2019'),
                ]),
            
            html.Br(),
            
            html.Div([
                dcc.Markdown(f'''# **Most affected countries, Totals, {l_words[4]}, {l_years[4]}:**'''),
                dcc.Markdown(id='markdown-top-3-total-2019')
                ]),
            ])

            ]),
    html.Br(),
    html.Hr(),
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='select-list-id-input', options=[i for i in range(len(l_of_lists))], value=0,
                          placeholder='select list of countries...'),
            html.Div(id='select-list-id-output', children=[]),
            dcc.Dropdown(id='select-country', options=[],
                          placeholder='select country...', 
                          multi=True),
            
            html.Br(),
            html.Br(),
            html.Br(),
            
            html.H2(f'Barchart -- {l_words[0]} -- {l_years[0]}'),
            dcc.Graph(id='Barchart-all-countries', figure={}),
            ]),
        
        dbc.Col([
            dcc.Dropdown(id='select-one-country-input', options=[],
                          placeholder='select country...'),
            
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            
            html.Div(id='select-one-country-output', children=[]),
            html.H2(f'Barchart -- {l_words[0]} -- {l_years[0]}'),
            dcc.Graph(id='Barchart-by-country', figure={})]),
        ]),
    ])


""" check if store works..."""                      
# @callback(
#     Output('words-output', 'children'),
#     Input('store-words', 'data')
#     )
# def return_val(data):
#     children = data[0]['Stroke']
    
#     print(f'type(data): {type(data)}')
#     print(f'data: {children}')
#     return children
                         
                         

@callback(
    [Output('full-table-2017', 'data'),
      Output('full-table-2017', 'columns'),
      Output('markdown-top-3-countries-2017', 'children'),
      Output('markdown-top-3-total-2017', 'children')],
    Input('store-1', 'data')
    )
def fn_full_table_2017(data):
    #print(f'type(data)-2017 ----- {type(data)}')
    
    df = pd.DataFrame(data)
    
    #print(f'columns: {df.columns}')
    df_top = df.sort_values(by=['Total'], ascending=False, ignore_index=True).iloc[1:4, :]
    #print(f'df_top: {df_top}')
    
    most_affected_countries = df_top.loc[:, 'Location'].to_list()
    most_affected_countries_total = df_top.loc[:, 'Total'].to_list()
    most_affected_countries_total = [int(nb) for nb in most_affected_countries_total]
    
    #print(f'data from 1rst callback: {df.head()}')
    records = df.to_dict('records')
    columns = [{"name": col, "id": col} for col in df.columns]
    
    
    #print(f'most_affected_countries: {most_affected_countries}')
    #print(f'most_affected_countries_total: {most_affected_countries_total}')
    
    text_string_countries = f'''  
    # 1. {most_affected_countries[0]}  
    # 2. {most_affected_countries[1]}  
    # 3. {most_affected_countries[2]}
    '''
    text_string_total = f''' 
    # 1. {most_affected_countries_total[0]}
    # 2. {most_affected_countries_total[1]}
    # 3. {most_affected_countries_total[2]}
    '''
    
    return records, columns, text_string_countries, text_string_total




@callback(
    [Output('full-table-2019', 'data'),
      Output('full-table-2019', 'columns'),
      Output('markdown-top-3-countries-2019', 'children'),
      Output('markdown-top-3-total-2019', 'children')],
    Input('store-4', 'data')
    )
def fn_full_table_2019(data):
    #print(f'type(data)-2019 ----- {type(data)}')
    
    df = pd.DataFrame(data)
    
    #print(f'columns: {df.columns}')
    df_top = df.sort_values(by=['Total'], ascending=False, ignore_index=True).iloc[1:4, :]
    #print(f'df_top: {df_top}')
    
    most_affected_countries = df_top.loc[:, 'Location'].to_list()
    most_affected_countries_total = df_top.loc[:, 'Total'].to_list()
    most_affected_countries_total = [int(nb) for nb in most_affected_countries_total]
    
    #print(f'data from 1rst callback: {df.head()}')
    records = df.to_dict('records')
    columns = [{"name": col, "id": col} for col in df.columns]
    
    
    #print(f'most_affected_countries: {most_affected_countries}')
    #print(f'most_affected_countries_total: {most_affected_countries_total}')
    
    text_string_countries = f'''  
    # 1. {most_affected_countries[0]}  
    # 2. {most_affected_countries[1]}  
    # 3. {most_affected_countries[2]}
    '''
    text_string_total = f''' 
    # 1. {most_affected_countries_total[0]}
    # 2. {most_affected_countries_total[1]}
    # 3. {most_affected_countries_total[2]}
    '''
    
    return records, columns, text_string_countries, text_string_total





@callback(
    Output('all-countries-2017', 'figure'),
    Input('store-1', 'data')
    )
def all_countries_2017(data):
    df = pd.DataFrame(data)
    #print(f'df from all countries ---- {df.head()}')
    df_all = df.iloc[0,1:-3]
    df_all_T = df_all.T
    #print(f'df_all_T.columns -- {df_all_T.columns}')
    #print(f'df_all_T ---- {type(df_all_T)}')
    
    fig_2017 = px.bar(df_all_T,
                  x=df_all_T.index,
                  y=df_all.values,
                  title='Total deaths, all countries, by age ranking'
                  )
    return fig_2017





@callback(
    Output('all-countries-2019', 'figure'),
    Input('store-4', 'data')
    )
def all_countries_2019(data):
    df = pd.DataFrame(data)
    #print(f'df from all countries ---- {df.head()}')
    df_all = df.iloc[0,1:-3]
    df_all_T = df_all.T
    #print(f'df_all_T.columns -- {df_all_T.columns}')
    #print(f'df_all_T ---- {type(df_all_T)}')
    
    fig_2019 = px.bar(df_all_T,
                  x=df_all_T.index,
                  y=df_all.values,
                  title='Total deaths, all countries, by age ranking'
                  )
    return fig_2019





@callback(
    Output('select-list-id-output', 'children'),
    Input('select-list-id-input', 'value')
    )
def return_select_output(value):
    #print(f'value in callback input: {value}')
    return value


@callback([
    Output('select-country', 'options'),
    Output('select-country', 'value')],
    [Input('select-list-id-output', 'children'),
     Input('store-list_dict','data')]
    )
def fn_select_list_id(value, data):
    value_output = []
    #print(f'value from select-list-id-output: {value}')
    #print(f'type(data): {type(data)}')
    
    list_of_options_output = data[value]
    
    
    #print(f'value: {value}')
    #print(f'list_of_options_output: {list_of_options_output}')
    
    for d in list_of_options_output:
        value_output.append(d['label'])
    #print(f'list of countries shown in dropdown: {value_output}')
    
            
    return list_of_options_output, value_output



@callback(
    Output('Barchart-all-countries', 'figure'),
    [Input('store-1', 'data'),
      Input('select-country', 'value')]
    )
def select_country(data, value):
    #print(f'value from select_country fn: {value}')
    df = pd.DataFrame(data) 
    #print(f'df from select_country: {df.head()}')
    new_df = df[df['Location'].isin(value)]
    #print(f'new_df: {new_df}')
            
    fig_country = px.bar(new_df,
                          x='Location',
                          y='Total', 
                          title='Total deaths by Country',
                          color='Location')
    return fig_country


@callback(
    [Output('select-one-country-input', 'options'),
      Output('select-one-country-input', 'value')],
    Input('select-list-id-output', 'children')
    )
def select_one_country(value):
    value_output = []
    #print(f'value from fn One Country: {value}')
    options_select_country = create_list_of_dict(list_of_dictionaries, n=12)
    list_of_options_output = options_select_country[value]
    
    #print(f'value: {value}')
    #print(f'list_of_options_output in One Country: {list_of_options_output}')
    
    for d in list_of_options_output:
        for key, val in d.items():
            value_output.append(d[key])
    #print(f'list of countries: {value_output}')
    #print(f'First value in value_output: {value_output[0]} ')
    
    first_country_value = value_output[0]
    
            
    return list_of_options_output, first_country_value



@callback(
    Output('Barchart-by-country', 'figure'),
    [Input('store-1', 'data'),
      Input('select-one-country-input', 'value')]
    )
def return_figure_desease_by_country(data, value):
    
    #print(f'data one country: {data}')
    #print(f'value fron One country: {value}')
    
    df = pd.DataFrame(data)
    df = df.copy()
    df = df.set_index('Location')
    #print(f'after reset index: {df}')
    
    df_one_country = df[df.index == value]
    
    y_values = df_one_country.iloc[:, :-4].values[0]
    y_values = list(y_values)
    
    x_values = df_one_country.iloc[:, :-4].columns
    # print(f'{len(y_values)}, -----, {len(x_values)}')
    
    d_ = {"age_ranking": x_values, "values": y_values}
    new_df = pd.DataFrame(d_)
    
    
    fig_one_country = px.bar(new_df,
                              x='age_ranking',
                              y='values',
                              color='age_ranking',
                              title='desease intensity effect by age ranking, by country')
    
    return fig_one_country
    










    
