import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
df = pd.read_csv('athlete_events.csv')
re_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,re_df)
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise analysis')

)
#st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    st.header('Medal Tally')
    year, country = helper.countary_Year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",year)
    selected_country = st.sidebar.selectbox("Select country",country)
    medal_tally = helper.fetch_data_metal_tally(df,selected_year,selected_country)
    st.dataframe(medal_tally)
if user_menu == 'Overall Analysis':

    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    event = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nation = df['region'].unique().shape[0]
    st.header('Top Statices')
    col1, col2 , col3 = st.columns(3)
    with col1 :
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sport")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Event")
        st.title(event)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("nation")
        st.title(nation)
    nation_over_time = helper.data_over_time(df,'region')
    fig = px.line(nation_over_time, x = "Edition" , y = "region")
    st.plotly_chart(fig)

    event_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(event_over_time, x="Edition", y="Event")
    st.plotly_chart(fig)

    Athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(Athlete_over_time, x = "Edition", y = "Name")
    st.plotly_chart(fig)

    st.title('No of Event over time (Every Sport)')
    fig,ax  = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index = 'Sport', columns = 'Year' , values = 'Event' , aggfunc = 'count').fillna(0).astype('int'),annot = True)
    st.pyplot(fig)

    st.title("Most successfull Atheletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select the sport', sport_list)
    x = helper.most_successful_sport(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis' :
    st.sidebar.title('Country wise list')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a country', country_list)
    country_df = helper.year_wise_medal_tally( df , selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title("Medal tally over the year")
    st.plotly_chart(fig)
    pt = helper.country_event_heatmap(df , selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap( pt , annot = True)
    st.pyplot(fig)
    top15_df = helper.most_successful_countrywise(df , selected_country)
    st.title("Top 15 athletes of" + selected_country)
    st.table(top15_df)

if user_menu == 'Athlete wise analysis':
    athlete_df = df.drop_duplicates(subset = ['Name' , 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall age', 'gold medalist', 'Sliver medalist', 'Bronze medalist'],show_hist = False , show_rug = False)
    st.title('Distribution of age')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    print(name)
    fig = ff.create_distplot(x, name, show_hist = False , show_rug = False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of age with sports")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df, x='Weight', y ='Height', s=60 , hue = 'Medal' , style = 'Sex')
    st.pyplot(fig)

    final = helper.men_v_wemon(df)
    fig = px.line(final , x = "Year" , y = ["Male","Female"])
    st.plotly_chart(fig)







