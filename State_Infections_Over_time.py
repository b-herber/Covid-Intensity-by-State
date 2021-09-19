# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 08:27:44 2021

@author: bherb
"""

import pandas as pd
import numpy as np
import os

import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser'
import chart_studio
import chart_studio.plotly as py

username = 'bherber' # your username
api_key = '8q8fJ4ESFQg2PG5xtoZb' # your api key - go to profile > settings > regenerate key
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)



os.getcwd()
dir = ('C:/Users/bherb/OneDrive/Documents/DataScience/Projects/Covid/')
os.chdir(dir)
os.listdir(dir)

# TODO NEEDS UPDATE prior to use: source: https://github.com/nytimes/covid-19-data Updated state level COVID data from NYTimes
state_inf = pd.read_csv('C:/Users/bherb/OneDrive/Documents/DataScience/Projects/Covid/us-states.csv')

# source: https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/counties/totals/ State population dataset from 2020 census
state_pop = pd.read_csv('C:/Users/bherb/OneDrive/Documents/DataScience/Projects/Covid/nst-est2020.csv',
                      encoding="ISO-8859-1")

state_code=pd.read_csv('C:/Users/bherb/OneDrive/Documents/DataScience/Projects/Covid/state-abbr-name.csv')

state_inf['date'] = pd.to_datetime(state_inf['date'])
state_inf['date'] = state_inf['date'].map(lambda x: x.strftime('%m/%d/%Y'))


state_pop_slim = state_pop[['STATE', 'NAME', 'POPESTIMATE2020']]

state_pop_slim = state_pop_slim[state_pop_slim['STATE'] != 0]
state_pop_slim = state_pop_slim[(state_pop_slim['NAME'] != 'District of Columbia')&(state_pop_slim['NAME'] != 'Puerto Rico')]



master = pd.merge(state_pop_slim, state_inf, how='left', left_on=['NAME'], right_on=['state'])
master = master.drop(['STATE', 'state'], axis=1)


master['New_Cases_Per_100000'] = master['cases'] / (master['POPESTIMATE2020'] / 100000)

master.dropna(inplace=True)
master = pd.merge(master, state_code, how='left', left_on=['NAME'], right_on=['State'])

master['date'] = pd.to_datetime(master['date'])
master['year']=pd.DatetimeIndex(master['date']).year
master['month']=pd.DatetimeIndex(master['date']).month

state_mnth_group = master.groupby(['NAME', 'year', 'month'])
state_inf_mnth = state_mnth_group.agg(Min_Infections=('cases', np.min), Max_Infections=('cases', np.max))


state_inf_mnth['New Cases'] = state_inf_mnth['Max_Infections'] - state_inf_mnth['Min_Infections']
state_inf_mnth = state_inf_mnth.reset_index()
state_inf_mnth['date']=pd.to_datetime(state_inf_mnth.year.astype(str)+ '/' + state_inf_mnth.month.astype(str) + '/28')
state_inf_mnth['date'] = state_inf_mnth['date'].map(lambda x: x.strftime('%m/%d/%Y'))

state_inf_mnth = pd.merge(state_inf_mnth, state_code, how='left', left_on=['NAME'], right_on=['State'])
state_inf_mnth = pd.merge(state_inf_mnth, state_pop_slim, how='left', left_on=['NAME'], right_on=['NAME'])
state_inf_mnth['New Cases Per 100000'] = state_inf_mnth['New Cases'] / (state_inf_mnth['POPESTIMATE2020'] / 100000)
state_inf_mnth = state_inf_mnth[(state_inf_mnth['date'] != '01/28/2020')&(state_inf_mnth['date'] != '02/28/2020')&(state_inf_mnth['date'] != '09/28/2021')]


fig=px.choropleth(state_inf_mnth, 
              locations = 'Code',
              color="New Cases Per 100000", 
              animation_frame="date",
              color_continuous_scale="Inferno",
              range_color=(0, 4470),
              locationmode='USA-states',
              scope="usa",
              title='Covid Infections by State',
              height=600
             )

fig.show()
py.plot(fig, filename = 'Covid by State', auto_open=True)


