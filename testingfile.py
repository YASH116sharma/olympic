if True:
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

    df = preprocessor.preprocess(df, re_df)
    st.sidebar.title("Olympics Analysis")
    user_menu = st.sidebar.radio(
        'Select an option',
        ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise analysis')

    )
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

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select the sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],hue = temp_df['Medal'] , style = temp_df['Sex'],s =100)
    st.pyplot(fig)