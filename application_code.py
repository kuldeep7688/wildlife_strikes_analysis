import streamlit as st
import altair as alt
import pandas as pd


# df = pd.read_csv('../../courses/cmse-830/datasets/faa_wildlife_strikes/main_data.csv')

# add introduction about the data 
# add FAA website link

# show the missing value heatmap 
# and mention the missing type 

st.write("""
# Aircraft Wildlife Strikes Data
### Analyzing the hidden aspects of the wildlife strikes data actively maintained by FAA
""")


year_range_values = st.slider(
    'Select a range of values',
    1990, 2022, (2000, 2010)
)
st.write('Values:', year_range_values)


options_time_of_day = st.multiselect(
    'What time of day are you interested in :',
    ['Day', 'Night', 'Dusk', 'Dawn'],
    ['Day', 'Night'])

st.write('You selected:', options_time_of_day)


# subset data according to the above filter

# add graph of airports and states with  most strikes  (Side by Side)
# add graph of airports and states with most damage 
# add graph of airports and states with most cost and compare with adjusted cost
