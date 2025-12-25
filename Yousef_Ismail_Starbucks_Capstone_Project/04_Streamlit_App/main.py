import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import date
import os

#load preprocessor and model


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
   BASE_DIR,
   "..",        
   "03_Data",
   "Processed_Data",
   "final_Cleaned_Data.csv")

try:
    data = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    st.error("Dataset file not found. Please check file location.")
    st.stop()


# with open('preprocess', "rb") as input_file:
#     preprocessor = cPickle.load(input_file)

# with open('demo', "rb") as input_file:
#     model = cPickle.load(input_file)

# data=pd.read_csv("final_Cleaned_Data.csv")
data["became_member"] = pd.to_datetime(data["became_member"]).dt.year
data["age_group"]=pd.cut(x=data["age"],bins=[18,30,40,50,60,70,80,100],
          labels=["18-30 age","30-40 age","40-50 age","50-60 age","60-70 age","70-80 age","80-above age"])
# streamlit layout

st.set_page_config(page_title="Prediction offers in Starbucks",layout="wide")

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "Pages",
    ("Info", "EDA")
)
#####################################################################################################################################

# Using "with" notation
if add_selectbox =="Info":
    st.title("Prediction offers in Starbucks mobile app, By [Yousef Ismail Ahmed](https://www.linkedin.com/in/yousef-ismail87/)")

                    
    st.header("About :")

    st.markdown("Overview: \n This data set contains simulated data that mimics customer behavior on the Starbucks rewards mobile app. Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free). Some users might not receive any offer during certain weeks. Not all users receive the same offer, and that is the challenge to solve with this data set. Your task is to combine transaction, demographic and offer data to determine which demographic groups respond best to which offer type. This data set is a simplified version of the real Starbucks app because the underlying simulator only has one product whereas Starbucks actually sells dozens of products. Every offer has a validity period before the offer expires. As an example, a BOGO offer might be valid for only 5 days. You'll see in the data set that informational offers have a validity period even though these ads are merely providing information about a product; for example, if an informational offer has 7 days of validity, you can assume the customer is feeling the influence of the offer for 7 days after receiving the advertisement. You'll be given transactional data showing user purchases made on the app including the timestamp of purchase and the amount of money spent on a purchase. This transactional data also has a record for each offer that a user receives as well as a record for when a user actually views the offer. There are also records for when a user completes an offer.")
    st.markdown("-----------------------------------")
    data=pd.read_csv("../03_Data/Processed_Data/final_Cleaned_Data.csv")
    

    st.markdown("This is the sample of dataframe after cleaning:")
    sample=st.dataframe(data.sample(15))
    btn=st.button("Display another sample")
    if btn:
        print(sample)


    st.markdown("-----------------------------------")

#####################################################################################################################################

if add_selectbox =="EDA":
    st.subheader("In Exploratory data analysis (EDA) we have 3 type")
    st.markdown("1) Univarate")
    st.markdown("2) Bivarate")
    st.markdown("3) Multivarate")
    sb=st.selectbox("__Select what type to show visualization it__",["Univarate","Bivarate","Multivarate"])
    #########################
    if sb== "Univarate":
        columns=data.columns.drop(["person","value/offer id","age_group"]).to_list()
        uni=st.selectbox("choose column : ",columns)
        ###########
        if uni=="gender":
            fig=px.bar(data_frame=data["gender"].value_counts().reset_index(),
                       x="gender",
                       y="count",
                       labels={"index":"gender","gender":"count"},
                       text_auto="0.2s")
            fig.update_traces(textfont_size=12,textposition="outside")
            fig.update_layout(title_text="count of gender",title_x=0.5)
            st.plotly_chart(fig)
        ###########
        if uni=="event":
            df=data.event.value_counts().reset_index()
            fig=px.bar(data_frame=df,x="event",y="count",text_auto="0.2s",
                labels={"index":"event",
                        "event":"count"})
            fig.update_traces(textfont_size=12,textposition="outside")
            fig.update_layout(title_text="count of event",title_x=0.5)
            st.plotly_chart(fig)
        ########### 
        if uni=="offer_type":
            df=data.offer_type.value_counts().reset_index()
            fig=px.bar(data_frame=df,x="offer_type",y="count",text_auto="0.2s",
                labels={"index":"offer_type",
                        "offer_type":"count"})
            fig.update_traces(textfont_size=12,textposition="outside")
            fig.update_layout(title_text="count of offer_type",title_x=0.5)
            st.plotly_chart(fig)
        ###########

        ###########
        #numerical
        numerical=data.select_dtypes(exclude="O").columns.to_list()
        for col in numerical:
            if uni==col:
                fig=px.histogram(data[col])
                fig.update_layout(title_text=f"Histgorm of {col}",title_x=0.5)
                st.plotly_chart(fig)
                break
        
    #########################
    if sb== "Bivarate":

        col1,col2,col3=st.columns(3)
        with col1:
            # event and offer_type
            df=data.groupby(["offer_type","event"]).agg({"event":"count"}).rename(columns={"event":"count"}).reset_index()
            fig=px.bar(data_frame=df,x="offer_type",y="count",color="event", barmode='group',text_auto="0.2s")
            fig.update_traces(textfont_size=12,textposition="outside")
            fig.update_layout(title_text="event VS offer_type",title_x=0.5)
            st.plotly_chart(fig)
        with col2:
            # gender and offer_type
            df=data.groupby(["offer_type","gender"]).agg({"gender":"count"}).rename(columns={"gender":"count"}).reset_index()
            fig=px.bar(data_frame=df,x="offer_type",y="count",color="gender", barmode='group',text_auto="0.2s")
            fig.update_traces(textfont_size=12,textposition="outside")
            fig.update_layout(title_text="gender VS offer_type",title_x=0.5)
            st.plotly_chart(fig)
        with col3:
            # age and offer_type
            df=data.groupby(["offer_type","age_group"]).agg({"age_group":"count"}).rename(columns={"age_group":"count"}).reset_index()
            fig=px.bar(data_frame=df,x="age_group",y="count",color="offer_type", barmode='group',text_auto="0.2s")
            fig.update_traces(textfont_size=12,textposition="outside")
            fig.update_layout(title_text="age VS offer_type",title_x=0.5)
            st.plotly_chart(fig)
            st.markdown("- age between 50 and 60 that have most vote in all offers")
        col1,col2=st.columns(2)
        with col1:
            # login_days and offer_type
            fig=px.box(data_frame=data,x="login_days",color="offer_type")
            fig.update_layout(title_text="login_days VS offer_type",title_x=0.5)
            st.plotly_chart(fig)
        with col2:
            # income and offer_type
            fig=px.box(data_frame=data,x="income",color="offer_type",)
            fig.update_layout(title_text="income VS offer_type",title_x=0.5)
            st.plotly_chart(fig)
    #########################
    if sb== "Multivarate":
        # gender , age_group and offer_type
        filtered_data = data[data["offer_type"] != "no_offer"]

        # age_group, gender, offer_type
        
        df=filtered_data.groupby(["age_group","gender","offer_type"]).agg({"offer_type":"count"}).rename(columns={"offer_type":"count"}).reset_index()
        fig=px.sunburst(data_frame=df,path=["age_group","gender","offer_type"],values="count")
        fig.update_traces(textinfo="label+percent entry")
        fig.update_layout(title_text="[age_group , gender] VS offer_type",title_x=0.5)
        st.plotly_chart(fig)
        st.markdown("- Most vote for age between 50 and 60 male and most vote in offers are bogo and discount")

        # gender , event and offer_type

        df=filtered_data.groupby(["event","gender","offer_type"]).agg({"offer_type":"count"}).rename(columns={"offer_type":"count"}).reset_index()
        fig=px.sunburst(data_frame=df,path=["event","gender","offer_type"],values="count")
        fig.update_traces(textinfo="label+percent entry")
        fig.update_layout(title_text="[event , gender] VS offer_type",title_x=0.5)
        st.plotly_chart(fig)
        st.markdown("- males that are recievied  offer of bogo those are most vote from last graph")

        #correlation
        numerical=data.select_dtypes(exclude="O").columns.drop("age_group").to_list()
        fig = px.imshow(data[numerical].corr(), text_auto='.2f')
        st.plotly_chart(fig)
        st.markdown("- __There are realation between :__")
        st.markdown("1) age - income")
        st.markdown("2) rewared - [ difficult , duration]")
        st.markdown("3) difficult - duration")
####################################################################################################################################
