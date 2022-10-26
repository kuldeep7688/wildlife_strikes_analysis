import streamlit as st
import altair as alt
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from utilities import preprocess_text_fields, remapping_function
from collections import Counter
st.set_page_config(layout="wide")

# Title and subtitle
st.write("""
# Aircraft Wildlife Strikes Data
#### Analyzing the hidden aspects of the wildlife strikes data actively maintained by FAA
""")

try:
    df = pd.read_csv('data/main_data.csv')
    print('df loading successful')
except:
    print('Something went wrong in loading data.')

# add introduction about the data 
st.write("""
### Introduction
- The FAA Wildlife Strike Database contains records of reported wildlife strikes since 1990.
Since the strike reporting is voluntary, this database only represents the information FAA 
has received from airlines, airports, pilots, and other sources. 
- There is an observed increase in the wildlife strikes on planes from 1990 to 2022. As a result, there
has been greater emphasis on wildlife strike hazard research and airfield wildlife management.

- This application is a window to diving deeper into the data and understanding the economical
aspects related to it. 
The dataset can be found at [FAA Wildlife strikes Data](https://wildlife.faa.gov/home).
""")

# ADD SEPARATOR

# some required preprocessing
df = preprocess_text_fields(df)
df = remapping_function(df)
columns_to_remove = [
    'NR_FATALITIES', 'NR_INJURIES', 'EFFECT_OTHER',  'LOCATION', 
    'ENG_1_POS', 'ENG_2_POS', 'ENG_3_POS', 'ENG_4_POS', 'LATITUDE', 'LONGITUDE', 
    # 'STR_RAD', 'DAM_RAD', 'STR_WINDSHLD', 'DAM_WINDSHLD', 'STR_NOSE', 'DAM_NOSE', 'STR_ENG1', 'DAM_ENG1', 'STR_ENG2', 
    # 'DAM_ENG2', 'STR_ENG3', 'DAM_ENG3', 'STR_ENG4', 'DAM_ENG4', 'STR_PROP', 'DAM_PROP', 'STR_WING_ROT', 'DAM_WING_ROT', 
    # 'STR_FUSE', 'DAM_FUSE', 'STR_LG', 'DAM_LG', 'STR_TAIL', 'DAM_TAIL', 'STR_LGHTS', 'DAM_LGHTS', 'STR_OTHER', 'DAM_OTHER',
]
df = df[[c for c in list(df.columns) if c not in columns_to_remove]]
df['INCIDENT_YEAR'] = pd.to_datetime(df["INCIDENT_YEAR"], format='%Y')

# showing of data and graphs and df.head
#   adding 4 tabs with total, small, medium and high damage and df.head
st.write(
    '''
    ##### Introduction Graphs and Dataframe
    '''
)
int_tab_1, int_tab_2, int_tab_3, int_tab_4, int_tab_5 = st.tabs(
    [
        'Total Strikes', 'Strikes with Small Birds',
        'Strikes with Medium or Large Birds',
        'Dataframe',
        'Initial Preprocessing Steps'
    ]
)
with int_tab_1:
    st.header('Total number of Wildlife Strikes through the years')
    temp_df = df.groupby(
        'INCIDENT_YEAR'
    )['INCIDENT_YEAR'].agg('count').to_frame('counts').reset_index()
    # plotting
    chart_1 = alt.Chart(temp_df).mark_line().encode(
        alt.X('INCIDENT_YEAR', axis=alt.Axis(format='%Y')),
        # x='INCIDENT_YEAR',
        alt.Y('counts'),
    )
    st.altair_chart(chart_1, use_container_width=True)

with int_tab_2:
    st.header('Total number of Strikes with small species through the years')
    temp_df = df[df.SIZE == 'Small'].groupby(
        'INCIDENT_YEAR'
    )['INCIDENT_YEAR'].agg('count').to_frame('counts').reset_index()
    # plotting
    chart_2 = alt.Chart(temp_df).mark_line().encode(
        alt.X('INCIDENT_YEAR', axis=alt.Axis(format='%Y')),
        # x='INCIDENT_YEAR',
        alt.Y('counts'),
    )
    st.altair_chart(chart_2, use_container_width=True)

with int_tab_3:
    st.header('Total number of Strikes with medium and large species throughthe years')
    temp_df = df[df.SIZE.isin(['Medium', 'Large'])].groupby(
        'INCIDENT_YEAR'
    )['INCIDENT_YEAR'].agg('count').to_frame('counts').reset_index()
    # plotting
    chart_3 = alt.Chart(temp_df).mark_line().encode(
        alt.X('INCIDENT_YEAR', axis=alt.Axis(format='%Y')),
        # x='INCIDENT_YEAR',
        alt.Y('counts'),
    )
    st.altair_chart(chart_3, use_container_width=True)

with int_tab_4:
    st.header('Dataset Display')
    num_rows_to_see = st.number_input(
        'Insert a number of rows you want to see:',
        min_value=1, max_value=100, value= 10
    )
    temp_df = df.sample(num_rows_to_see)
    st.dataframe(temp_df)

with int_tab_5:
    st.header('Initial Preprocessing Steps :')
    st.write(
        '''
        1) Preprocessing text fields and converting empty strings to None values after going through the
            field information.
        2) Remapping classes of ordinal and nominal variables.
        3) Converting fields to a particular datatype instead of object dataype.
        4) Normalizing null values all across the dataframe as 'None' has a different meaning in some of the columns.
        '''
    )

# show the missing value heatmap 
st.write(
    '''
    #### HeatMap for assessing missingness type.
    Info : Since data is too big showing map on randomly sampled 50k subset.
    '''
)
# m_df = df.sample(50000)
# missing_value_heatmap = plt.figure(figsize=(20,20))
# sns.heatmap(m_df.isna().transpose(), cmap="viridis")
# st.pyplot(missing_value_heatmap)
# and mention the missing type 
st.write(
    '''
    #### Observations :
    1) Cost related fields have a lot of Null values
    2) NUM_SEEN, WARNED, EFFECT also have fairly high number of Null values.
    3) Missingness type is Missingness at Random, as most of the values can be inferred from other fields using rules.
    - Some suggestions are provided to fill the missing values.
    '''
)

# subsetting the data by taking values from the user
st.write(
    '''
    #### Please select the Range for years you are interested in :
    '''
)
year_range_values = st.slider(
    '',
    1990, 2022, (2000, 2010), label_visibility='hidden'
)
# ADD SEPARATOR

df = df[
    (df['INCIDENT_YEAR'] >= pd.to_datetime(year_range_values[0], format='%Y')) & 
    (df['INCIDENT_YEAR'] <= pd.to_datetime(year_range_values[1], format='%Y'))
]
print('dataframe shape after subsetting for year is : {}'.format(df.shape))


# asking the user about the time of day he/she is in interested in
st.write(
    '''
    #### What time of day are you interested in:
    '''
)
options_time_of_day = st.multiselect(
    '',
    ['Day', 'Night', 'Dusk', 'Dawn'],
    ['Day', 'Night', 'Dusk', 'Dawn']
)
# ADD SEPARATOR

df = df[df['TIME_OF_DAY'].isin(options_time_of_day)]
print('dataframe shape after subsetting for time of day is : {}'.format(df.shape))

# Dive into Airport Analysis
st.write(
    '''
    #### Airport Analysis of 100 Airports with most Strikes
    '''
)
# air_tab_1, air_tab_2, air_tab_3, air_tab_4 = st.tabs(
#     [
#         'Number of Strikes during the period selected:', 
#         'Number of Strikes with distinction in Damage Level',
#         'Number of Strikes with Minor or Substantial Damage',
#         'Damage Level Trends'
#     ]
# )

# # selecting 100 most count airports
# hundred_most_ws_airports = [
#     i[0] for i in Counter(df[df.AIRPORT != 'UNKNOWN'].AIRPORT.to_list()).most_common(100)
# ]
# with air_tab_1:
#     st.write('#### Number of Strikes at top 100 Airports')
#     chart_5 = alt.Chart(df[df.AIRPORT.isin(hundred_most_ws_airports)]).mark_bar(size=10).encode(
#         x='AIRPORT:N',
#         y='count()',
#         # column='DAMAGE_LEVEL:N',
#     ).properties(
#         width=1500,
#         height=500
#     )
#     st.altair_chart(chart_5, use_container_width=True)


# with air_tab_2:
#     st.write('#### Number of Strikes at top 100 Airports with Damage Level')
#     chart_6 = alt.Chart(df[df.AIRPORT.isin(hundred_most_ws_airports)]).mark_bar(size=10).encode(
#         x='AIRPORT:N',
#         y='count()',
#         color='DAMAGE_LEVEL:N',
#     ).properties(
#         width=1500,
#         height=500
#     )
#     st.altair_chart(chart_6, use_container_width=True)


# with air_tab_3:
#     temp_df = df[df.DAMAGE_LEVEL.isin(['Substantial', 'Destroyed'])]
#     hundred_most_ws_airports = [
#         i[0] for i in Counter(temp_df[temp_df.AIRPORT != 'UNKNOWN'].AIRPORT.to_list()).most_common(100)
#     ]
#     st.write('#### Number of Strikes at top 100 Airports with Damage Level Substantial or Destroyed')
#     chart_7 = alt.Chart(temp_df[temp_df.AIRPORT.isin(hundred_most_ws_airports)]).mark_bar(size=10).encode(
#         x='AIRPORT:N',
#         y='count()',
#         color='DAMAGE_LEVEL:N',
#     ).properties(
#         width=1500,
#         height=500
#     )
#     st.altair_chart(chart_7, use_container_width=True)

# with air_tab_4:
#     temp_df = df[['INCIDENT_YEAR', 'DAMAGE_LEVEL']].groupby('INCIDENT_YEAR').agg(
#         no_damage=('DAMAGE_LEVEL', lambda x: Counter(x)['No_Damage']),
#         minor_damage=('DAMAGE_LEVEL', lambda x: Counter(x)['Minor']),
#         substantial_damage=('DAMAGE_LEVEL', lambda x: Counter(x)['Substantial']),
#         destroyed=('DAMAGE_LEVEL', lambda x: Counter(x)['Destroyed'])
#     ).reset_index()
#     temp_df = temp_df.melt(id_vars=['INCIDENT_YEAR'], value_vars=['minor_damage', 'substantial_damage', 'destroyed'])
#     chart_8 = alt.Chart(temp_df).mark_line().encode(
#         alt.X('INCIDENT_YEAR', axis=alt.Axis(format='%Y')),
#         y='value:Q',
#         color='variable:N'
#     )
#     st.altair_chart(chart_8, use_container_width=True)

st.write(
    '''
    #### Observations :
    1)
    2) 
    3)
    '''
) 


st.write(
    '''
    ### Phase of Flight Analysis
    '''
)
# phase of flight with with number of birds and damage level analysis
ph_tab_1, ph_tab_2, ph_tab_3 = st.tabs(
    [
        'PHASE_OF_FLIGHT Counts', 
        'Phase of Flight with Number of birds struck',
        'Phase of flight with number of birds struct and damage level',
    ]
)

with ph_tab_1:
    st.write('#### Phase of Flight')
    chart_9 = alt.Chart(df).mark_bar().encode(
        x='PHASE_OF_FLIGHT:N',
        y='count()',
    ).properties(
        width=1500,
        height=500
    ).interactive()
    st.altair_chart(chart_9, use_container_width=True)

with ph_tab_2:
    st.write('#### Phase of Flight with Number of birds struck')
    chart_10 = alt.Chart(df).mark_bar().encode(
        x='PHASE_OF_FLIGHT:N',
        y='count()',
        color='NUM_STRUCK'
    ).properties(
        width=1500,
        height=500
    ).interactive()
    st.altair_chart(chart_10, use_container_width=True)


with ph_tab_3:
    st.write('#### Phase of Flight with Num of Birds and Damage Level')
    chart_11 = alt.Chart(df).mark_bar().encode(
        x='PHASE_OF_FLIGHT:N',
        y='count()',
        color='NUM_STRUCK',
        column='DAMAGE_LEVEL'
    ).interactive()
    st.altair_chart(chart_11)

st.write(
    '''
    #### Observations :
    1)
    2) 
    3)
    '''
) 
# add graph of airports and states with most cost and compare with adjusted cost
