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
model_path = os.path.join(os.path.dirname(__file__), "aml_final.pkl")
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

        prediction_method = st.radio('', ('Predict Record-wise', 'Predict for Entire DataFrame'))
        if prediction_method=='Predict Record-wise':
            c1, c2, c3 = st.columns([1, 1, 1.5])
            
            with c1:
                st.markdown('<p style="color:red;">Timestamp EX:2022/09/01 00:20</p>', unsafe_allow_html=True)
                timestamp = st.text_input("YYYY/MM/DD HH:MM", key='timestamp')
            
                st.markdown('<p style="color:red;">From Bank</p>', unsafe_allow_html=True)
                from_bank = st.text_input("", key='from_bank')
            
                st.markdown('<p style="color:red;">From Account</p>', unsafe_allow_html=True)
                from_account = st.text_input("", key='from_account')
            
            with c2:
                st.markdown('<p style="color:red;">To Bank</p>', unsafe_allow_html=True)
                to_bank = st.text_input("", key='to_bank')
            
                st.markdown('<p style="color:red;">To Account</p>', unsafe_allow_html=True)
                to_account = st.text_input("", key='to_account')
            
                st.markdown('<p style="color:red;">Amount Received</p>', unsafe_allow_html=True)
                amount_received = st.number_input("", key='amount_received')
            
            with c3:
                st.markdown('<p style="color:red;">Receiving Currency</p>', unsafe_allow_html=True)
                receiving_currency = st.selectbox("",['US Dollar', 'Bitcoin', 'Euro', 'Australian Dollar', 'Yuan','Rupee', 'Mexican Peso', 'Yen', 'UK Pound', 'Ruble','Canadian Dollar', 'Swiss Franc', 'Brazil Real', 'Saudi Riyal', 'Shekel'], key='receiving_currency')
            
                st.markdown('<p style="color:red;">Amount Paid</p>', unsafe_allow_html=True)
                amount_paid = st.number_input("", key='amount_paid')
            
                st.markdown('<p style="color:red;">Payment Currency</p>', unsafe_allow_html=True)
                payment_currency = st.selectbox("", ['US Dollar', 'Bitcoin', 'Euro', 'Australian Dollar', 'Yuan','Rupee', 'Yen', 'Mexican Peso', 'UK Pound', 'Ruble', 'Canadian Dollar', 'Swiss Franc', 'Brazil Real', 'Saudi Riyal','Shekel'], key='payment_currency')
            
                st.markdown('<p style="color:red;">Payment Format</p>', unsafe_allow_html=True)
                payment_format = st.selectbox("", ['Reinvestment', 'Cheque', 'Credit Card', 'ACH', 'Cash', 'Wire','Bitcoin'], key='payment_format')
            
            # Extracting time-related features from the timestamp

            data =[[timestamp, from_bank, from_account, to_bank, to_account, amount_received, 
                     receiving_currency, amount_paid, payment_currency, payment_format]]
            
            columns = ["time stamp", "from bank", "account", "to bank", "account.1", "amount received", 
                            "receiving currency", "amount paid", "payment currency", "payment format"]
        


            try:
                df = pd.DataFrame(data, columns=columns)
            
                    
                
                
                df["time stamp"] = pd.to_datetime(df["time stamp"])

                    
                l_account=esin_list = [
                '100428660', '1004286a8', '100428660', '100428780', '100428660', '100428738', 
                '1004287c8', '1004286a8', '1004286f0', '100428780', '100428738', '1004287c8', 
                '1004286a8', '1004288e8', '1004289c0', '100428780', '100428978', '100428738', 
                '1004286f0', '1004287c8', '100428660', '100428660', '1004286a8', '1004286a8', 
                '100428660', '80266f880', '812d22980', '1004286a8', '811c599a0', '811c597b0', 
                '8021353d0', '100428978', '100428a51', '812a09d40', '812d0c3c0', '811b6e170', 
                '811b83280', '812a09cf0', '80452d470', '800737690', '100428660', '1004286a8', 
                '100428978', '80266f880', '100428810', '812d22980', '100428738', '811c597b0', 
                '811c599a0', '8021353d0', '1004286f0', '100428780', '812a09d40', '100428a51', 
                '811b83280', '812d0c3c0', '812a09cf0', '1004288a0', '811b6e170', '1004287c8'
]
                df["currency_focus"]=df["account"].apply(lambda x: "focus" if x in l_account else "not focus")

                l_pf=payment_methods = [
                'cheque', 'cheque', 'cash', 'cheque', 'credit card', 'cheque', 'cheque', 'cash', 
                'cheque', 'credit card', 'credit card', 'credit card', 'credit card', 'cheque', 
                'cheque', 'cash', 'cheque', 'cash', 'credit card', 'cash', 'cheque', 'credit card', 
                'cheque', 'credit card', 'cash', 'ach', 'ach', 'cash', 'ach', 'ach', 'ach', 
                'cheque', 'bitcoin', 'ach', 'ach', 'ach', 'ach', 'ach', 'ach', 'ach'
    ]
                df["pf_focus"]=df["payment format"].apply(lambda x: "focus" if x in l_pf else "not focus")


                l_pc=['saudi riyal','euro',
                                'euro',
                                'euro',
                                'canadian dollar',
                                'yen',
                                'yuan',
                                'rupee',
                                'us dollar',
                                'us dollar']
            
                df["pc_focus"]=df["payment currency"].apply(lambda x: "focus" if x in l_pc else "not focus")

                l_rc=['us dollar',
                'euro',
                'swiss franc',
                'euro',
                'uk pound',
                'saudi riyal',
                'yen',
                'saudi riyal',
                'saudi riyal',
                'euro',
                'yuan',
                'rupee',
                'saudi riyal',
                'bitcoin',
                'saudi riyal',
                'saudi riyal',
                'saudi riyal',
                'australian dollar',
                'saudi riyal',
                'ruble']
            
                df["rc_focus"]=df["receiving currency"].apply(lambda x: "focus" if x in l_rc else "not focus")

                l_account_1=[
                '811c599a0', '8021353d0', '811c597b0', '80266f880', '811ed7df0', '812a09cf0', 
                '811d80c30', '811b83280', '80aebecb0', '8079ddc30', '8028f2650', '809cc4600', 
                '80465e020', '8106b1750', '80098dc70', '800924840', '812a09d40', '805d4c850', 
                '8012cd590', '80c6f48a0'
            ]
                df["account.1_focus"]=df["account.1"].apply(lambda x: "focus" if x in l_account_1 else "not focus")

                df["day"]=df["time stamp"].dt.day
                df["hour"]=df["time stamp"].dt.hour
                df["min"]=df["time stamp"].dt.minute
                df['day_type'] = df['time stamp'].dt.dayofweek.apply(lambda x: 'weekday' if x < 5 else 'weekend')
                df['day_of_week'] = df['time stamp'].dt.day_name()


                level1=[1,2,3,4,5,6,7,8,9,10,]
                level2=[11,12,13,14]
                level3=[15,16,17,18]



                def intensity(x):
                                if x in level1:
                                    return "high"
                                elif x in level2:
                                    return "medium"
                                else:
                                    return "low"
                df["day_intensityy"]=df["day"].apply(intensity)

                df.drop("time stamp",axis=1,inplace=True)


                



                

               
                    
                
                    
            except ValueError:
                st.error("Incorrect timestamp format. Please use YYYY-MM-DD HH:MM:SS.")


            
            
            


            
           
            
           

######################################################

            
            if sum(list(df.isnull().sum().values)) == 0:
                
                if st.button("Predict"):
                    with st.spinner("Please wait while predicting...."):
                        time.sleep(0.5)
                    
                        try:
                            result = model.predict(df)
                            if result[0] == 0:
                                st.markdown('<h2 style="color:red;">Not laundering** 🎉😊</h2>', unsafe_allow_html=True)

                                
                            else:
                                st.markdown('<h2 style="color:red;">Laundering** 😞</h2>', unsafe_allow_html=True)

                                
                                st.toast('bad luck', icon="👎")
                        except Exception as e:
                            st.error(f"An error occurred during prediction: {e}")
            else:
                st.markdown('<p style="color:red;">Please Enter All The Fields</p>', unsafe_allow_html=True)

                 
                
                
        else:
            st.markdown('<p style="color:red;">Select file type</p>', unsafe_allow_html=True)

    
            file_type = st.selectbox("", ("CSV", "Excel"))
            #uploaded_file=None


    
            uploaded_file = st.file_uploader(f"Upload {file_type} file",type=[file_type.lower()])

            if file_type=="CSV":

                try:
                    df=pd.read_csv(uploaded_file)
                    df.to_csv("df.csv",index=False)
                except Exception as e:
                                st.write("Not Uploaded")
            else:
                try:
                    df=pd.read_excel(uploaded_file)
                    df.to_excel("df.xlsx",index=False)

                except Exception as e:
                                st.write("Not Uploaded")

                
    
            #with c1:
            if st.button("Predict"):
                with st.spinner("Please wait while predicting...."):
                    time.sleep(1)
                
                
                    try:
                        result = model.predict(df)
                        laundering = ["Yes" if pred == 1 else "No" for pred in result]
                        df["laundering"] = laundering
    
                        l_counts = df['laundering'].value_counts()
    
                        st.markdown(f'<p style="color:orange; font-weight:bold;">No of Transactions Laundering: {l_counts["Yes"]}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p style="color:orange; font-weight:bold;">Toatl No of Transactions: {len(laundering)}</p>', unsafe_allow_html=True)
                        st.title("Go to Prediction Analytics to view analytics")
                                
    
    
                    except Exception as e:
                            st.error("Please upload your file before predicting...")
                    
                
                    


elif selected == "Prediction Analytics":


    import matplotlib.pyplot as plt
    import seaborn as sns
    import streamlit as st

    data=False



   
    with st.container():
         st.title('Transactions Analysis...........')
    try:
         df = pd.read_csv("df.csv")
         data=True
    except Exception as e:
         st.title("You Have No Any Prediction yet")

    if data:
        
        c11, c22 = st.columns([1,0.2])
        with c11:
            filtered_df = df[df["is laundering"] == 1]
            top_to_banks_counts = filtered_df["to bank"].value_counts().head(20)
            top_to_banks_df = top_to_banks_counts.reset_index()
            top_to_banks_df.columns = ["to bank", "count"]
            plt.figure(figsize=(12, 6))
            sns.barplot(x="to bank", y="count", data=top_to_banks_df)
            plt.xticks(rotation=90)
            plt.title("Top 20 Destination Banks by Laundering Activity (is laundering = 1)")
            plt.xlabel("To Bank")
            plt.ylabel("Laundering Count")
            st.pyplot(plt)
        with c22:
            st.dataframe(top_to_banks_df,height=700)
    
        with c11:
            filtered_df = df[df["is laundering"] == 1]
            top_from_banks_counts = filtered_df["from bank"].value_counts().head(20)
            top_from_banks_df = top_from_banks_counts.reset_index()
            top_from_banks_df.columns = ["from bank", "count"]
            plt.figure(figsize=(12, 6))
            sns.barplot(x="from bank", y="count", data=top_from_banks_df)
            plt.xticks(rotation=90)
            plt.title("Top 20 Sender Banks by Laundering Activity (is laundering = 1)")
            plt.xlabel("from Bank")
            plt.ylabel("Laundering Count")
            st.pyplot(plt)
    
        with c22:

            st.dataframe(top_from_banks_df,height=600)
        with c11:
           payment_format_counts = df[df["is laundering"] == 1]["payment format"].value_counts()
           payment_format_counts_df = payment_format_counts.reset_index()
           payment_format_counts_df.columns = ["payment format", "count"]
           plt.figure(figsize=(10, 6))
           sns.barplot(x="payment format", y="count", data=payment_format_counts_df)
           plt.xticks(rotation=90)
           plt.title("Laundering Activity by Payment Format")
           plt.xlabel("Payment Format")
           plt.ylabel("Count")
           st.pyplot(plt)
        with c22:
            st.dataframe(payment_format_counts_df,height=850)
        with c11:
            currency_counts = df[df["is laundering"] == 1]["payment currency"].value_counts()
            currency_counts_df = currency_counts.reset_index()
            currency_counts_df.columns = ["payment currency", "count"]
            
            plt.figure(figsize=(10, 6))
            sns.barplot(x="payment currency", y="count", data=currency_counts_df)
            plt.xticks(rotation=90)
            plt.title("Laundering Activity by Payment Currency")
            plt.xlabel("Payment Currency")
            plt.ylabel("Count")
            
            st.pyplot(plt)
        with c22:
            st.dataframe(currency_counts_df,height=900)
        with c11:

            receiving_currency_counts = df[df["is laundering"] == 1]["receiving currency"].value_counts()
            receiving_currency_counts_df = receiving_currency_counts.reset_index()
            receiving_currency_counts_df.columns = ["receiving currency", "count"]
            
            plt.figure(figsize=(10, 6))
            sns.barplot(x="receiving currency", y="count", data=receiving_currency_counts_df)
            plt.xticks(rotation=90)
            plt.title("Laundering Activity by Receiving Currency")
            plt.xlabel("Receiving Currency")
            plt.ylabel("Count")
            
            st.pyplot(plt)
        with c22:
            st.dataframe(receiving_currency_counts_df)
          

            




       
            
            


            
    


