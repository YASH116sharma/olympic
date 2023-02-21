import numpy as np

import helper


def medal_tally(df):
    m_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    m_tally = m_tally.groupby('NOC').sum()[['Gold' , 'Silver','Bronze' ]].sort_values('Gold', ascending = False).reset_index()
    m_tally['Total'] = m_tally['Bronze'] + m_tally['Gold'] + m_tally['Silver']
    m_tally['Gold'] = m_tally['Gold'].astype('int')
    m_tally['Silver'] = m_tally['Silver'].astype('int')
    m_tally['Bronze'] = m_tally['Bronze'].astype('int')
    m_tally['Total'] = m_tally['Total'].astype('int')
    return m_tally

def countary_Year_list(df):
    m_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    countaries = np.unique(df['region'].dropna().values).tolist()
    countaries.sort()
    countaries.insert(0 , 'Overall')
    return years, countaries

def fetch_data_metal_tally(df,year,country):
  m_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
  flag =0
  if year == 'Overall' and country == 'Overall':
    temp_df = m_tally
  if year != 'Overall' and country == 'Overall':
    temp_df = m_tally[m_tally['Year'] == int(year)]
  if year == 'Overall' and country != 'Overall':
    flag = 1
    temp_df = m_tally[m_tally['region'] == country]
  if year != 'Overall' and country != 'Overall':
    temp_df = m_tally[ (m_tally['Year'] == year) & (m_tally ['region']== country)]
  temp_df['Total'] = temp_df['Bronze'] + temp_df['Gold'] + temp_df['Silver']
  if flag == 1:
    x = temp_df.groupby('Year').sum()[['Gold' , 'Silver','Bronze']].sort_values('Gold', ascending = False).reset_index()
  else :
    x = temp_df.groupby('region').sum()[['Gold' , 'Silver','Bronze']].sort_values('Gold', ascending = False).reset_index()
  x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
  x['Gold'] = x['Gold'].astype('int')
  x['Silver'] = x['Silver'].astype('int')
  x['Bronze'] = x['Bronze'].astype('int')
  x['Total'] = x['Total'].astype('int')

  return x

def data_over_time( df,col ):
    data_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    data_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return data_over_time

def most_successful_sport(df, sport):

    temp_df = df.dropna(subset = ['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(35).merge(df , left_on = 'index' , right_on = 'Name' , how = 'left')[
        ['index', 'Name_x', 'Sport','region' ]
    ].drop_duplicates('index')
    x.rename( columns = {'index' : 'Name' , 'Name_x': 'Medals'},inplace = True)
    return x

def year_wise_medal_tally( df , country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event','Medal'])
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index = 'Sport', columns = 'Year' , values = 'Medal', aggfunc = 'count').fillna(0).astype('int')
    return pt

def most_successful_countrywise(df, country):

    temp_df = df.dropna(subset = ['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df , left_on = 'index' , right_on = 'Name' , how = 'left')[
        ['index', 'Name_x', 'Sport' ]
    ].drop_duplicates('index')
    x.rename( columns = {'index' : 'Name' , 'Name_x': 'Medals'},inplace = True)
    return x
def weight_v_height(df , sport):
    athlete_df = df.drop_duplicates(subset = ['Name' , 'region'])
    athlete_df['Medal'].fillna('No medal', inplace = True)
    temp_df = athlete_df
    if sport != 'Overall':
       temp_df = athlete_df[athlete_df['Sport'] == sport]
    return temp_df

def men_v_wemon(df):
    athelet_df = df.drop_duplicates(subset = ['Name', 'region'])
    men = athelet_df[athelet_df['Sex']== 'M'].groupby('Year').count()['Name'].reset_index()
    women = athelet_df[athelet_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women , on = 'Year' , how = 'left')
    final.fillna(0, inplace = True)
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    return final