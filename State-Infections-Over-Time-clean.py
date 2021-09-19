# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 10:48:19 2021

@author: bherb
"""

import pandas as pd
import plotly.io as pio
import plotly.express as px

#this will open the animation in your default browser
pio.renderers.default='browser'

#update relative path here to CSV file
state_inf_mnth=pd.read_csv('C:/Users/bherb/OneDrive/Documents/DataScience/Projects/Covid/state_inf_mnth.csv')

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