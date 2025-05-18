from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import streamlit as st
import time
import base64
from sqlalchemy import create_engine,text
import pymysql
from sqlalchemy.exc import SQLAlchemyError
from xgboost import XGBClassifier
import re



import os
model_path = os.path.join(os.path.dirname(__file__), "aml_finall.pkl")
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error(f"Model file {model_path} not found.")
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
####################################################################################


df=None
def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()




st.set_page_config(layout="wide")

# Custom CSS to remove padding and margins

# these are the internal dinamic classes genrating during running and we are making them padding 0
# style for inserting the css script
# unsafe_allow_html=True to insert the html and css into the streamlit
# markdown is to exicute the css and html into the streamlit

custom_css = """
    <style>
    .css-1d391kg, .css-1v3fvcr, .css-18e3th9 {
        padding: 0 !important;
    }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)



# Navigation menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",  # required
        options=["Home", "Prediction Analytics"],  # required
        icons=["house", "bar-chart"],  # optional
         menu_icon="box-arrow-in-right",
        default_index=0,  # optional
    )

# Pages based on selected option
if selected == "Home":
        bg_image_path = r"aml_bg1.png"
        bg_image_base64 = get_base64_of_bin_file(bg_image_path)
        st.markdown(f"""
        <style>
        .stApp {{

            background-image: url("data:image/jpg;base64,{bg_image_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """, unsafe_allow_html=True)
        dic={}

        #st.title("**anti money laundering**")
        st.markdown('<h2 style="color:yellow;">Anti-Money Laundering (AML) Detection </h2>', unsafe_allow_html=True)


        st.markdown('<h4 style="color:orange;">Select Prediction Method</h4>', unsafe_allow_html=True)

        st.markdown("""
                    <style>
                    div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
                        color: gold !important;
                        font-weight: bold;
                    }
                    </style>
                """, unsafe_allow_html=True)

       



      


            
            
            


            
           
            
 

    
                
    
    
                  

elif selected == "Prediction Analytics":


    import matplotlib.pyplot as plt
    import seaborn as sns
    import streamlit as st

           
       
            




       
            
            


            
    


