import streamlit as st
import pandas as pd
import altair as alt
pd.options.display.float_format = '{:.1f}'.format 


groupby_domains = pd.read_csv('DATA/Domains clustered.csv')
daily_data = pd.read_csv('DATA/Global Report.csv')

st.title('Find the domains that fit better to your campaign ')



st.header('This is the test to offer to the advertisers the domains that fit better in their campaigns')

st.sidebar.header('User Input Parameters')

if st.sidebar.button('Press for info'):
    st.write('Has apretado')

panel = st.sidebar.selectbox('Choose a panel', ( "User free use", "Recommendations"))
if panel == "User free use" :

    #Region filtering

    st.markdown('### Region filter')
    regions = groupby_domains['Geographical zone'].unique()
    regions_selected= st.multiselect('In wich region/s do you want to deploy your campaign?', regions)
    st.write('You selected', len(regions_selected), 'regions')

    region_filter = groupby_domains[groupby_domains['Geographical zone'].isin(regions_selected)].iloc[:,2:13]


    #Categories filtering
    st.markdown('### Category filter')
    categories = region_filter['Category'].unique()
    categories_selected = st.multiselect('Select the categories you are interested on', categories)
    categories_filter = region_filter[region_filter['Category'].isin(categories_selected)].iloc[:,0:11]


    #Order by filtering
    columns = categories_filter.columns.unique()
    order_selected= st.selectbox('Choose the parameter to order by', columns)

    orderby_filter = categories_filter.sort_values(by= order_selected, ascending=False).reset_index(drop=True)

    #Displaying the tendency grapghs of the domain:
    def trend_graphs(data):
        trend_line_formatloads = alt.Chart(data).mark_line(color='#F18727').encode(
            x="yearmonth(Time):T",
            y="mean(Format Loads)",
        ).properties(
            title="Anual Format Loads tendency",
            height=200,
            width = 500).interactive()

        trend_line_formatfillrate = alt.Chart(data).mark_line(color='green').encode(
            x="yearmonth(Time):T",
            y="mean(Format Fill Rate)",
        ).properties(
            title="Anual Format Loads Rate tendency",
            height=200,
            width = 500).interactive()

        trends_domain =  trend_line_formatloads & trend_line_formatfillrate

        st.altair_chart(trends_domain, use_container_width=True)

    st.write('### Filtered domains', orderby_filter)
    selected_indices = st.multiselect('Select Domains by row:', orderby_filter.index)
    selected_rows = orderby_filter.loc[selected_indices]
    st.write('### Selected Domains', selected_rows)
    group_historic=daily_data[daily_data['Domain']==domain_search]

    if st.checkbox('Show the tendencies of the selected group'):
        #Displaying the tendency grapghs of the domain:
        trend_graphs(group_historic)

    domain_search = st.text_input('Enter the name of the Domain','Type here')


    if st.button('Submit'):

        domain=groupby_domains[groupby_domains['Domain']==domain_search]
        domain_historic=daily_data[daily_data['Domain']==domain_search]
        #Warning if the registered domain historic is less than 80% of days
        if domain_historic.shape[0]<292:
            st.warning('There is no a constant historic of this domain')
            #Displaying the table of the domain selected:
            st.write(domain.iloc[:,2:])
            #Displaying the trend graphs
            trend_graphs(domain_historic)

        elif domain_historic.shape[0]>292:
            st.write('These are the characteristics over the last 366 days')
            #Displaying the table of the domain selected:
            st.write(domain.iloc[:,2:])
            #Displaying the trend graphs
            trend_graphs(domain_historic)

        else:
            st.warning('This domain is not registered, try again!')

else:
    st.write('Has elegido lo otro')


#interactive dataframe
# st.dataframe(groupby_domains.style.highlight_max(axis=0))
#def user_input_features():
    #format_loads=st.sidebar.slider('Format Loads', 1,2000000,(100000, 200000), step=29999)
    #impressions=st.sidebar.slider('Impressions', 1,100000,(5000, 10000), step=5000)
    #data={'Format Loads':format_loads, 'Impressions':impressions}
    #features=pd.DataFrame(data)

    #return features
#df=user_input_features()
#st.write(df)

#st.exception('NameError('Name three not defined')"