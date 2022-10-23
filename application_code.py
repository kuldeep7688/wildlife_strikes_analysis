import streamlit as st
import altair as alt
import pandas as pd


# Title and subtitle
st.write("""
# Aircraft Wildlife Strikes Data
#### Analyzing the hidden aspects of the wildlife strikes data actively maintained by FAA
""")

try:
    df = pd.read_csv('../../courses/cmse-830/datasets/faa_wildlife_strikes/main_data.csv')
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
df['INCIDENT_YEAR'] = pd.to_datetime(df["INCIDENT_YEAR"], format='%Y')

# showing of data and graphs and df.head
#   adding 4 tabs with total, small, medium and high damage and df.head
st.write(
    '''
    ##### Introduction Graphs and Dataframe
    '''
)
int_tab_1, int_tab_2, int_tab_3, int_tab_4 = st.tabs(
    [
        'Total Strikes', 'Strikes with Small Birds',
        'Strikes with Medium or Large Birds',
        'Dataframe'
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

# show the missing value heatmap 
# and mention the missing type 

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

# add graph of airports and states with  most strikes  (Side by Side)
# add graph of airports and states with most damage 
# add graph of airports and states with most cost and compare with adjusted cost
