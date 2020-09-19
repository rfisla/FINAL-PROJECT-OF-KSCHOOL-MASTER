#STREAMLIT APP - DOMAINS RECOMMENDATION

import streamlit as st
import pandas as pd
import altair as alt



groupby_domains = pd.read_csv('Domains clustered.csv')

@st.cache
def load_daily_data():
    return pd.read_csv('Daily Report.csv')
daily_data = load_daily_data()


st.title(":chart_with_upwards_trend: DIGITAL ADVERTISING ANALYTICS")


st.header('**Reach the right target market for your campaign**')

st.sidebar.header(":gear: PANELS")


#Function to display the trend graphs

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

#DIPLAYING THE TWO MAIN PANELS
panel = st.sidebar.selectbox('Choose a panel', ( "Free use", "Recommendations"))

            
#USER FREE USE PANEL
if panel == "Free use":
    st.markdown('##  *Free use panel*')

    #Region filtering
    st.write('### :earth_americas: Region filter')
    regions = groupby_domains['Geographical zone'].unique()
    regions_selected= st.multiselect('In wich region/s do you want to deploy your campaign?', regions)
    st.write('You selected', len(regions_selected), 'regions')

    region_filter = groupby_domains[groupby_domains['Geographical zone'].isin(regions_selected)].iloc[:,2:]


    #Categories filtering
    st.markdown('### :books: Category filter')
    categories = region_filter['Category'].unique()
    categories_selected = st.multiselect('Select the categories you are interested in', categories)
    categories_filter = region_filter[region_filter['Category'].isin(categories_selected)].iloc[:,0:]


    #Order by filtering and displaying the filtered DF

    st.write('This selection has', len(categories_filter),' domains.')

    columns = categories_filter.columns.unique()
    order_selected= st.selectbox('Choose the parameter to order by', columns)

    orderby_filter = categories_filter.sort_values(by= order_selected, ascending=False).reset_index(drop=True)
    
    st.write('### :mag_right: Filtered domains', orderby_filter)

    #Button with the information about the columns
    if st.checkbox('Press for info about the columns'):
        st.markdown('- **Domain**: website.\n'
        '- **Format Loads:** The traffic of the Domain.\n'
        '- **Impressions:**  The number of times that the ad plays (views).\n'
        '- **Format Fill Rate**: Impressions / Format Loads.  This displays the total fill rate of Format tag loads.\n'
        '- **CPM:**  (Cost Per Milli) Cost per one thousand impressions.\n'
        '- **Clicks:**  The number of clicks in the ad recorded, (when the user goes to the website of the advertiser throught the video).\n'
        '- **CTR:**  (Click Through Rate) Clicks / Impressions.\n'
        '- **Viewability Rate:** Percentage of impressions where the video displayed more than 70%.\n'
        '- **Category:** Category of the domain.\n'
        '- **Country:** The country where most traffic of the domain comes from.\n'
        '- **Geographical zone:** The region of the country.\n')


    #Selecting row by row the desirable group

    selected_indices = st.multiselect('Customize your group of Domains selecting by index:', orderby_filter.index)
    selected_rows = orderby_filter.loc[selected_indices]
    
    st.write('### :clipboard:Final selection', selected_rows)
    
    #Displaying the tendency grapghs of the domain in a hide box:
    if st.checkbox('Show the average tendencies and the main statistics of the selected group'):
        domains_selected = selected_rows['Domain']
        group_historic = daily_data[daily_data['Domain'].isin(domains_selected)]
        trend_graphs(group_historic)
        st.write('**Main statistics**', selected_rows.describe())

    #Individualized Domain Search

    st.markdown('## **Individualized Domain Search**')
    domain_search = st.text_input('Enter the name','')
    

    if st.button('Submit'):

        domain=groupby_domains[groupby_domains['Domain']==domain_search]
        domain_historic=daily_data[daily_data['Domain']==domain_search]
        #Warning if the registered domain historic is less than 80% of days
        if 1<domain_historic.shape[0]<292:
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
        #Warning if the registered domain is not registered
        else:
            st.warning('This domain is not registered, try again!')

#RECOMMENDATIONS PANEL
else:
    st.markdown('## *Recommendations panel*')

     #Region filter
    st.write('### :earth_americas: Region')
    panel_region = st.selectbox('Choose a Region', ("", "South America", "Others"))
    #Category filter
    st.markdown('### :books: Category filter')
    panel_category = st.selectbox('Choose a Category', ("", "News & Portals", "Others"))

 
 #CLUSTER 2
    
    if (panel_region == "South America") & (panel_category=="News & Portals"):
        cluster2= pd.read_csv('Global Cluster 2.csv')
        panel_fl2 = st.selectbox('Choose a range of daily traffic', ('20.000-80.000', '80.000-160.000','160.000-300.000','300.000-500.000',
                                                          '500.000-800.000', '800.000-1.000.000'))

        def cluster2_operations(data):
            
            st.write('The recommended group has', len(data),' domains.')
            st.write('You can order by any variable clicking in the name column')
            st.dataframe(data.iloc[:,2:])

            #Displaying the tendency grapghs of the table in a hidden box::
            if st.checkbox('Show the average tendencies and main statistics of the recommended group'): 
                recommended_group = data['Domain']
                recommended_group_historic = daily_data[daily_data['Domain'].isin(recommended_group)]
                trend_graphs(recommended_group_historic)
                st.write('**Main statistics**', data.iloc[:,1:].describe())
            
            #Selecting the desirable domains
            
            selected_indices = st.multiselect('Customize your own selection selecting by index:', data.index)
            selected_rows = data.loc[selected_indices]
            st.write('### Selected Domains', selected_rows)
            


            #Displaying the tendency grapghs of the domains selected in a hidden box:
            if st.checkbox('Show the average tendencies and main statistics of the selected group'):
                domains_selected = selected_rows['Domain']
                group_historic = daily_data[daily_data['Domain'].isin(domains_selected)]
                trend_graphs(group_historic)
                st.write(selected_rows.describe())
        
        #Adding the subclusters
        if panel_fl2 ==  '20.000-80.000':
            sub1 = cluster2[cluster2['Subcluster']==3].reset_index(drop=True)
            cluster2_operations(sub1)    

        elif panel_fl2 ==  '80.000-160.000':
            sub6 = cluster2[cluster2['Subcluster']==2].reset_index(drop=True)
            cluster2_operations(sub6) 

        elif panel_fl2 ==  '160.000-300.000':
            sub4 = cluster2[cluster2['Subcluster']==6].reset_index(drop=True)
            cluster2_operations(sub4) 

        elif panel_fl2 ==  '300.000-500.000':
            sub2 = cluster2[cluster2['Subcluster']==1].reset_index(drop=True)
            cluster2_operations(sub2)

        elif panel_fl2 ==  '500.000-800.000':
            sub5 = cluster2[cluster2['Subcluster']==5].reset_index(drop=True)
            cluster2_operations(sub5)

        else:
            sub3 = cluster2[cluster2['Subcluster']==4].reset_index(drop=True)
            cluster2_operations(sub3)                   
    
 #CLUSTER 1   

    elif (panel_region == "Others") & (panel_category=="News & Portals"):
        cluster1= pd.read_csv('Global Cluster 1.csv')
        panel_fl1 = st.selectbox('Choose a range of daily traffic', ('20.000-90.000', '130.000-220.000','220.000-460.000',
                                                          '500.000-725.000', '840.000-1.000.000', '1.700.000'))

        def cluster1_operations(data):
            
            #Filter by region
            regions = data['Geographical zone'].unique()
            regions_selected= st.multiselect('In wich region/s do you want to deploy your campaign?', regions)
            region_filter = data[data['Geographical zone'].isin(regions_selected)].iloc[:,2:].reset_index(drop=True)

            st.write('The recommended group has', len(region_filter),' domains.')
            st.write('You can order by any variable clicking in the name column')
            st.dataframe(region_filter)

            if st.checkbox('Show the average tendencies and main statistics of the recommended group'):
                recommended_group = region_filter['Domain']
                recommended_group_historic = daily_data[daily_data['Domain'].isin(recommended_group)]
                trend_graphs(recommended_group_historic)
                st.write('**Main statistics**', region_filter.iloc[:,1:].describe())
            
            #Selecting the desirable domains
            selected_indices = st.multiselect('Customize your own selection selecting by index:', region_filter.index)
            selected_rows = region_filter.loc[selected_indices]
            st.write('### Selected Domains', selected_rows)
            #Displaying the tendency grapghs of the domains selected in a hide box:
            
            if st.checkbox('Show the average tendencies and main statistics of the selected group'):
                domains_selected = selected_rows['Domain']
                group_historic = daily_data[daily_data['Domain'].isin(domains_selected)]
                trend_graphs(group_historic)
                st.write(selected_rows.describe())
    
        #Adding the subclusters:
        if panel_fl1 ==  '20.000-90.000':
            sub3 = cluster1[cluster1['Subcluster']== 1]
            cluster1_operations(sub3)    

        elif panel_fl1 ==  '130.000-220.000':
            sub1 = cluster1[cluster1['Subcluster']== 5]
            cluster1_operations(sub1) 

        elif panel_fl1 ==  '220.000-460.000':
            sub6 = cluster1[cluster1['Subcluster']== 3]
            cluster1_operations(sub6) 

        elif panel_fl1 ==  '500.000-725.000':
            sub4 = cluster1[cluster1['Subcluster']== 6]
            cluster1_operations(sub4)

        elif panel_fl1 ==  '840.000-1.000.000':
            sub2 = cluster1[cluster1['Subcluster']== 2]
            cluster1_operations(sub2)

        else:
            sub5 = cluster1[cluster1['Subcluster']== 4]
            cluster1_operations(sub5)        

 #CLUSTER 4   

    elif (panel_region == "South America") & (panel_category=="Others"):
        cluster4= pd.read_csv('Global Cluster 4.csv')
        panel_fl4 = st.selectbox('Choose a range of daily traffic', ('20.000-110.000', '110.000-315.000',
                                                          '350.000-600.000', '700.000-1.050.000'))
        def cluster4_operations(data):
            
            #Filtering by category
            categories = data['Category'].unique()
            categories_selected = st.multiselect('Select the categories you are interested on', categories)
            categories_filter = data[data['Category'].isin(categories_selected)].iloc[:,2:].reset_index(drop=True)
            
            st.write('The recommended group has', len(categories_filter),' domains.')
            st.write('You can order by any variable clicking in the name column')
            st.dataframe(categories_filter)

            if st.checkbox('Show the average tendencies and main statistics of the recommended group'):
                recommended_group = categories_filter['Domain']
                recommended_group_historic = daily_data[daily_data['Domain'].isin(recommended_group)]
                trend_graphs(recommended_group_historic)
                st.write('**Main statistics**', categories_filter.iloc[:,1:].describe())
            
            #Selecting the desirable domains
            selected_indices = st.multiselect('Customize your own selection selecting by index:', categories_filter.index)
            selected_rows = categories_filter.loc[selected_indices]
            st.write('### Selected Domains', selected_rows)
            #Displaying the tendency grapghs of the domains selected in a hide box:
            
            if st.checkbox('Show the average tendencies and main statistics of the selected group'):
                domains_selected = selected_rows['Domain']
                group_historic = daily_data[daily_data['Domain'].isin(domains_selected)]
                trend_graphs(group_historic)
                st.write(selected_rows.describe())
        
        #Adding the subclusters:
        if panel_fl4 ==  '20.000-110.000':
            sub3 = cluster4[cluster4['Subcluster']== 1]
            cluster4_operations(sub3)    

        elif panel_fl4 ==  '110.000-315.000':
            sub1 = cluster4[cluster4['Subcluster']== 4]
            cluster4_operations(sub1) 

        elif panel_fl4 ==  '350.000-600.000':
            sub6 = cluster4[cluster4['Subcluster']== 3]
            cluster4_operations(sub6) 

        else:
            sub4 = cluster4[cluster4['Subcluster']== 2]
            cluster4_operations(sub4)

 #CLUSTER 3   

    elif (panel_region == "Others") & (panel_category=="Others"):
        cluster3= pd.read_csv('Global Cluster 3.csv')


        def cluster3_operations(data):
            
            #Filtering by region
            regions = data['Geographical zone'].unique()
            regions_selected= st.multiselect('In wich region/s do you want to deploy your campaign?', regions)

            region_filter = data[data['Geographical zone'].isin(regions_selected)].iloc[:,2:]
            
            #Filtering by category
            categories = region_filter['Category'].unique()
            categories_selected = st.multiselect('Select the categories you are interested on', categories)
            categories_filter = region_filter[region_filter['Category'].isin(categories_selected)].reset_index(drop=True)
            
            st.write('The recommended group has', len(categories_filter),' domains.')
            st.write('You can order by any variable clicking in the name column.')
            st.dataframe(categories_filter)

            if st.checkbox('Show the average tendencies and main statistics of the recommended group'):
                recommended_group = categories_filter['Domain']
                recommended_group_historic = daily_data[daily_data['Domain'].isin(recommended_group)]
                trend_graphs(recommended_group_historic)
                st.write('**Main statistics**', categories_filter.iloc[:,1:].describe())
            
            #Selecting the desirable domains
            selected_indices = st.multiselect('Customize your own selection selecting by index:', categories_filter.index)
            selected_rows = categories_filter.loc[selected_indices]
            st.write('### Selected Domains', selected_rows)
        
            #Displaying the tendency grapghs of the domains selected in a hide box:
            if st.checkbox('Show the average tendencies and main statistics of the selected group'):
                domains_selected = selected_rows['Domain']
                group_historic = daily_data[daily_data['Domain'].isin(domains_selected)]
                trend_graphs(group_historic)
                st.write(selected_rows.describe())
            
        panel_fl3 = st.selectbox('Choose a range of daily traffic', ('20.000-65.000', '65.000-150.000','150.000-270.000','280.000-500.000',
                                                          '630.000-920.000', '2.700.000'))
        #Adding the subclusters:
     
        if panel_fl3 ==  '20.000-65.000':
            sub5 = cluster3[cluster3['Subcluster']== 2]
            cluster3_operations(sub5)    

        elif panel_fl3 ==  '65.000-150.000':
            sub1 = cluster3[cluster3['Subcluster']== 6]
            cluster3_operations(sub1) 

        elif panel_fl3 ==  '150.000-270.000':
            sub6 = cluster3[cluster3['Subcluster']== 1]
            cluster3_operations(sub6) 

        elif panel_fl3 ==  '280.000-500.000':
            sub3 = cluster3[cluster3['Subcluster']== 5]
            cluster3_operations(sub3)

        elif panel_fl3 ==  '630.000-920.000':
            sub4 = cluster3[cluster3['Subcluster']== 4]
            cluster3_operations(sub4)

        else:
            sub2 = cluster3[cluster3['Subcluster']== 3]
            cluster3_operations(sub2) 
    





