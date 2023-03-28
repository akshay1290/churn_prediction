import numpy as np
import pickle
import pandas as pd
import seaborn as sns 
import matplotlib.ticker as mtick  
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from imblearn.combine import SMOTEENN

from sklearn import preprocessing
#from flasgger import Swagger
import streamlit as st 



from PIL import Image



pickle_in = open("model_rf_smote.pkl", "rb")
model_rf_smote=pickle.load(pickle_in)


def welcome():
    return "Welcome All"


def predict_note_authentication(gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges):
    

   
    prediction=model_rf_smote.predict([[gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges]])
    print(prediction)
    return prediction



def main():

    image = Image.open('images/icone.png')
    image2 = Image.open('images/image.png')
    st.image(image,use_column_width=False)
    add_selectbox = st.sidebar.selectbox(
	"How would you like to predict?",
	("Online", "Batch"))
    st.sidebar.info('This app is created to predict Customer Churn')
    st.sidebar.image(image2)
    st.title("Predicting Customer Churn")
    if add_selectbox == 'Online':
                    
            gender = st.selectbox('gender', ['male', 'female'])
            SeniorCitizen= st.selectbox('SeniorCitizen', [0, 1])
            Partner= st.selectbox('Partner', ['yes', 'no'])
            Dependents = st.selectbox('Dependents', ['yes', 'no'])
            PhoneService = st.selectbox(' Customer has phoneservice:', ['yes', 'no'])
            MultipleLines = st.selectbox(' Customer has multiplelines:', ['yes', 'no', 'no_phone_service'])
            InternetService= st.selectbox(' Customer has internetservice:', ['dsl', 'no', 'fiber_optic'])
            OnlineSecurity= st.selectbox(' Customer has onlinesecurity:', ['yes', 'no', 'no_internet_service'])
            OnlineBackup = st.selectbox(' Customer has onlinebackup:', ['yes', 'no', 'no_internet_service'])
            DeviceProtection = st.selectbox(' Customer has deviceprotection:', ['yes', 'no', 'no_internet_service'])
            TechSupport = st.selectbox(' Customer has techsupport:', ['yes', 'no', 'no_internet_service'])
            StreamingTV = st.selectbox(' Customer has streamingtv:', ['yes', 'no', 'no_internet_service'])
            StreamingMovies = st.selectbox(' Customer has streamingmovies:', ['yes', 'no', 'no_internet_service'])
            Contract= st.selectbox(' Customer has a contract:', ['month-to-month', 'one_year', 'two_year'])
            PaperlessBilling = st.selectbox(' Customer has a paperlessbilling:', ['yes', 'no'])
            PaymentMethod= st.selectbox('Payment Option:', ['bank_transfer_(automatic)', 'credit_card_(automatic)', 'electronic_check' ,'mailed_check'])
            tenure = st.number_input('Number of months the customer has been with the current telco provider :', min_value=0, max_value=240, value=0)
            MonthlyCharges= st.number_input('Monthly charges :', min_value=0, max_value=240, value=0)
            TotalCharges = tenure*MonthlyCharges
            

            output= ""
            output_prob = ""


            if st.button("Predict"):
                from sklearn.preprocessing import LabelEncoder

                # Create a LabelEncoder object
                le = LabelEncoder()
               
    
                # Convert categorical variables to numerical values
                gender = le.fit_transform([gender])[0]
                SeniorCitizen = int(SeniorCitizen)
                Partner = le.fit_transform([Partner])[0]
                Dependents = le.fit_transform([Dependents])[0]
                PhoneService = le.fit_transform([PhoneService])[0]
                MultipleLines = le.fit_transform([MultipleLines])[0]
                InternetService = le.fit_transform([InternetService])[0]
                OnlineSecurity = le.fit_transform([OnlineSecurity])[0]
                OnlineBackup = le.fit_transform([OnlineBackup])[0]
                DeviceProtection = le.fit_transform([DeviceProtection])[0]
                TechSupport = le.fit_transform([TechSupport])[0]
                StreamingTV = le.fit_transform([StreamingTV])[0]
                StreamingMovies = le.fit_transform([StreamingMovies])[0]
                Contract = le.fit_transform([Contract])[0]
                PaperlessBilling = le.fit_transform([PaperlessBilling])[0]
                PaymentMethod = le.fit_transform([PaymentMethod])[0]

                    
                

               

             
                
                
                result=predict_note_authentication(gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges)
               
                y_pred = model_rf_smote.predict_proba([[gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges]])[0, 1]
                churn = y_pred >= 0.5
                output_prob = float(y_pred)
                output = bool(churn)
            st.success('Churn: {0}, Risk Score: {1}'.format(output, output_prob))
    if add_selectbox == 'Batch':
            file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])
            if file_upload is not None:
                data = pd.read_csv(file_upload)
                # Preprocessing
                # Encode categorical variables as numerical
                from sklearn.preprocessing import LabelEncoder
                encoder = LabelEncoder()
                for col in data.columns:
                    if data[col].dtype == 'object':
                        data[col] = encoder.fit_transform(data[col].astype(str))
                y_pred = model_rf_smote.predict_proba(data)[0, 1]
                churn = y_pred >= 0.5
                output_prob = float(y_pred)
                output = bool(churn)
                st.write(output)
            st.success('Churn: {0}, Risk Score: {1}'.format(output, output_prob))

if __name__=='__main__':
    main()
    
    
    