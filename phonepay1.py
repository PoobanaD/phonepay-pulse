#!/usr/bin/env python
# coding: utf-8

# In[6]:


# !pip install mysql-connector-python
# !pip install streamlit plotly mysql-connector-python
# !pip install streamlit
# !pip install streamlit_extras


# In[1]:


import mysql.connector 
import pandas as pd
#import psycopg2
import streamlit as st
import PIL 
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import requests
import geopandas as gpd
# connect to the database
import mysql.connector


# In[2]:


#establishing the connection
conn = mysql.connector.connect(user='root', password='12345', host='127.0.0.1', database="phonepe_pulse")


# In[3]:


# create a cursor object
cursor = conn.cursor()


# In[4]:


#with st.headbar:
SELECT = option_menu(
    menu_title = None,
    options = ["About","Home","Top Charts","Explore Data","Contact"],
    icons =["exclamation-circle","house","bar-chart","toggles","at"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "grey","size":"cover", "width": "100"},
        "icon": {"color": "black", "font-size": "20px"},
            
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}})


# In[5]:


#----------------Home----------------------#
cursor = conn.cursor()


# In[6]:


# execute a SELECT statement
cursor.execute("SELECT * FROM phonepe_pulse.data_aggregated_transaction_table")


# In[7]:


# fetch all rows
rows = cursor.fetchall()
from streamlit_extras.add_vertical_space import add_vertical_space


# In[8]:


if SELECT == "Home":
    col1,col2, = st.columns(2)
    col1.image(Image.open(r"C:\Users\Hari\Desktop\phone_pay.png"),width = 300)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")


# In[10]:


#----------------TOP CHARTS----------------------#

        # MENU 2 - TOP CHARTS
if SELECT == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.8],gap="medium")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )


# In[11]:


# Top Charts - TRANSACTIONS
if Type == "Transactions":
        col1,col2 = st.columns([1,1],gap="medium")
        
        with col1:
            st.markdown("### :violet[State]")
            cursor.execute(f"select state, sum(Total_Transactions_count) as Total_Transactions_Count, sum(Total_Amount) as Total from phonepe_pulse.data_aggregated_transaction_table where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions_count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Transactions_count'],
                             labels={'Total_Transactions_count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
       
        
        


# In[12]:


if Type == "Users":
        col1,col2,col3 = st.columns([2,2,2],gap="medium")
        
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                cursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(f"select district, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
              
            
        with col3:
            st.markdown("### :violet[State]")
            cursor.execute(f"select state, sum(Registereduser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


# In[13]:


#----------------EXPLORE DATA----------------------#

        
# MENU 3 - EXPLORE DATA
if SELECT == "Explore Data":
    Year = st.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.slider("Quarter", min_value=1, max_value=4)
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
    
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            cursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r"C:\\Users\\arunk\\OneDrive\\Desktop\\Statenames.csv")
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=True)
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            cursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r"C:\\Users\\arunk\\OneDrive\\Desktop\\Statenames.csv")
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)


# In[33]:


# BAR CHART - TOP PAYMENT TYPE
st.markdown("## :violet[Top Payment Type]")
cursor.execute(f"select Transacton_type, sum(Total_Transactions_count) as Total_Transactions, sum(Total_Amount) as Total_amount from phonepe_pulse.data_aggregated_transaction_table where year= {Year} and quarter = {Quarter} group by Transacton_type order by Transacton_type")
df = pd.DataFrame(cursor.fetchall(), columns=['Transacton_type', 'Total_Transactions','Total_amount'])

fig = px.bar(df,
                     title='Transacton Types vs Total_Transactions',
                     x="Transacton_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
st.plotly_chart(fig,use_container_width=False)
        


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




