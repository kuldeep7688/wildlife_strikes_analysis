import altair as alt
import numpy as np
import pandas as pd


# column types
# types of columns
CONTINUOUS_COLUMNS = [ # has both float and int columns
    'INDX_NR', 'LATITUDE', 'LONGITUDE', 
    'NUM_ENGS', 'ENG_1_POS', 'ENG_2_POS', 'ENG_3_POS', 'ENG_4_POS', # are ordered columns too
    'HEIGHT', 'SPEED', 'DISTANCE', 'AOS', 'COST_REPAIRS', 'COST_OTHER', 'COST_REPAIRS_INFL_ADJ', 'COST_OTHER_INFL_ADJ',
    'NR_INJURIES', 'NR_FATALITIES', 
    
]

NOMINAL_COLUMNS = [
    'TIME_OF_DAY', 'STATE', 'AIRPORT', 'AIRPORT_ID', 'FAAREGION', 'OPID', 'OPERATOR', 'REG', 'AIRCRAFT', 'EMA', 'EMO',
    'AMA', 'AMO', 'AC_CLASS', 'AC_MASS', 'TYPE_ENG', 'PHASE_OF_FLIGHT', 'SKY', 'PRECIPITATION', 'SPECIES_ID', 'SPECIES',
    
]

ORDINAL_COLUMNS = [
    'DAMAGE_LEVEL', 'NUM_SEEN', 'NUM_STRUCK', 'SIZE'
]

TEXT_COLUMNS = [
    'LOCATION', 
    'FLT', # specific to airlines can be explored further.,
    'EFFECT', 'EFFECT_OTHER', 
]

BOOLEAN_COLUMNS = [
    'INDICATED_DAMAGE', 'STR_RAD', 'DAM_RAD', 'STR_WINDSHLD', 'DAM_WINDSHLD', 'STR_NOSE', 'DAM_NOSE', 'STR_ENG1', 'DAM_ENG1', 
    'STR_ENG2', 'DAM_ENG2', 'STR_ENG3', 'DAM_ENG3', 'STR_ENG4', 'DAM_ENG4', 'STR_PROP', 'DAM_PROP', 'STR_WING_ROT', 'DAM_WING_ROT', 
    'STR_FUSE', 'DAM_FUSE', 'STR_LG', 'DAM_LG', 'STR_TAIL', 'DAM_TAIL', 'STR_LGHTS', 'DAM_LGHTS', 'STR_OTHER', 'DAM_OTHER',
    'WARNED',
]

DATETIME_COLUMNS = [
    'INCIDENT_DATE ', 'INCIDENT_MONTH', 'INCIDENT_YEAR', 'TIME',
]


# mapping dictionaries
PRECIPITATION_MAPPING = {
    'Rain': 'Rain',
    'Fog': 'Fog',
    'Snow': 'Snow',
    'None': 'No_precipitation',
    'Fog, Rain': 'Fog_plus_Rain',
    'Rain, Snow': 'Rain_plus_Snow',
    'Fog, Rain, Snow': 'Fog_plus_Rain_plus_Snow',
    'Fog, Snow': 'Fog_plus_Snow',
    'Snow, None': 'Snow',
    'Fog, None': 'Fog',
    'Rain, None': 'Rain',
    'Rain, Snow, None': 'Rain_plus_Snow'
}

DAMAGE_LEVEL_MAPPING = {
    'N': 'No_Damage',
    'S': 'Substantial',
    'M': 'Minor',
    'M?': 'Minor',
    'D': 'Destroyed'
}

EFFECT_MAPPING = {
    'None': 'No_Effect',
    'None, Aborted Take-off': 'Aborted Take-off', 
    'None, Precautionary Landing': 'Precautionary Landing', 
    'Precautionary Landing': 'Precautionary Landing', 
    'Other': 'Precautionary Landing', 
    'None, Other': 'Other', 
    'Aborted Take-off': 'Aborted Take-off', 
    'None, Engine Shutdown': 'Engine Shutdown', 
    'Engine Shutdown': 'Engine Shutdown', 
    'Precautionary Landing, Engine Shutdown': 'Precautionary Landing with Engine Shutdown', 
    'Precautionary Landing, Other': 'Precautionary Landing', 
    'None, Precautionary Landing, Engine Shutdown': 'Precautionary Landing with Engine Shutdown',
    'None, Precautionary Landing, Other': 'Precautionary Landing', 
    'None, Aborted Take-off, Other': 'Aborted Take-off', 
    'None, Aborted Take-off, Engine Shutdown': 'Aborted Take-off with Engine Shutdown', 
    'None, Aborted Take-off, Engine Shutdown, Other': 'Aborted Take-off with Engine Shutdown', 
    'None, Precautionary Landing, Engine Shutdown, Other': 'Precautionary Landing with Engine Shutdown', 
    'Aborted Take-off, Engine Shutdown': 'Aborted Take-off with Engine Shutdown'
}

WARNED_MAPPING = {
    'Yes': 'Yes',
    'No': 'No',
    'Unknown': np.nan,
}

AC_MASS_MAPPING = {
    '1.0': '<= 2250 kg', 
    '2.0': '2251 to 5700 kg',
    '3.0': '5701-27000 kg', 
    '4.0': '27001-272000 kg', 
    '5.0': '> 272000 kg', 
}

TYPE_ENGINE_MAPPING = {
    'D': 'Turbofan', 
    'C': 'Turboprop',
    'F': 'Turboshaft (helicopter)',
    'A': 'Reciprocating Engine', 
    'B': 'Turbojet', 
    'Y': 'Other', 
    'E': 'No_Engine'
}


# for all nominal, ordinal, text and INCIDENT_DATE and TIME strip the strings and make empty string as None
def text_preprocess_helper_func(x):
    if x == x:
        if x == str:
            return x.strip()
        else:
            return str(x).strip()
    else:
        return x


def preprocess_text_fields(df):
    # print('''
    # \n\n\n
    # Preprocessing happening.
    # \n\n\n
    # ''')
    columns_to_be_stripped = NOMINAL_COLUMNS + TEXT_COLUMNS + ['INCIDENT_DATE', 'TIME', 'NUM_STRUCK', 'NUM_SEEN']
    for col in columns_to_be_stripped:
        # print(col)
        df[col] = df[col].apply(text_preprocess_helper_func)
    
    # now convertinf empty strings to None values
    for col in columns_to_be_stripped:
        df.loc[df[col] == '', col] = np.nan
    
    return df


# remapping precipitation
def map_to_provided_labels(x, mapping):
    if x == x:
        return mapping[x]
    else:
        return x

def remapping_function(df):
    df['PRECIPITATION'] = df.PRECIPITATION.apply(lambda x : map_to_provided_labels(x, PRECIPITATION_MAPPING))
    df['DAMAGE_LEVEL'] = df.DAMAGE_LEVEL.apply(lambda x : map_to_provided_labels(x, DAMAGE_LEVEL_MAPPING))
    df['EFFECT'] = df.EFFECT.apply(lambda x : map_to_provided_labels(x, EFFECT_MAPPING))
    df['WARNED'] = df.WARNED.apply(lambda x : map_to_provided_labels(x, WARNED_MAPPING))
    df['AC_MASS'] = df.AC_MASS.apply(lambda x : map_to_provided_labels(x, AC_MASS_MAPPING))
    df['TYPE_ENG'] = df.TYPE_ENG.apply(lambda x : map_to_provided_labels(x, TYPE_ENGINE_MAPPING))
    return df


def altair_jointplot_speed_and_height(df, color_column, opacity=0.3):
    base = alt.Chart(df)
    xscale = alt.Scale(domain=(0.0, 340.0))
    yscale = alt.Scale(domain=(0.0, 16500.0))
    bar_args = {'opacity': opacity, 'binSpacing': 0}
    points = base.mark_circle().encode(
        alt.X('SPEED', scale=xscale),
        alt.Y('HEIGHT', scale=yscale),
        color=color_column,
    ).interactive()

    top_hist = base.mark_bar(**bar_args).encode(
        alt.X('SPEED:Q',
            # when using bins, the axis scale is set through
            # the bin extent, so we do not specify the scale here
            # (which would be ignored anyway)
            bin=alt.Bin(maxbins=20, extent=xscale.domain),
            stack=None,
            title=''
            ),
        alt.Y('count()', stack=None, title=''),
        alt.Color('{}:N'.format(color_column)),
    ).properties(height=60).interactive()

    right_hist = base.mark_bar(**bar_args).encode(
        alt.Y('HEIGHT:Q',
            bin=alt.Bin(maxbins=20, extent=yscale.domain),
            stack=None,
            title='',
            ),
        alt.X('count()', stack=None, title=''),
        alt.Color('{}:N'.format(color_column)),
    ).properties(width=60).interactive()
    return top_hist & (points | right_hist)


def get_correlation_graph(df, col_list):
    cor_data = (df[col_list]).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'})
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
    cor_data.head()
    base = alt.Chart(cor_data).encode(
        x='variable2:O',
        y='variable:O'    
    )

    # Text layer with correlation labels
    # Colors are for easier readability
    text = base.mark_text().encode(
        text='correlation_label',
        color=alt.condition(
            alt.datum.correlation > 0.5, 
            alt.value('white'),
            alt.value('black')
        )
    ).properties(
        width=1000,
        height=1000
    ).interactive()

    # The correlation heatmap itself
    cor_plot = base.mark_rect().encode(
        color='correlation:Q'
    ).properties(
        width=1000,
        height=1000
    ).interactive()

    return cor_plot + text # The '+' means overlaying the text and rect layer