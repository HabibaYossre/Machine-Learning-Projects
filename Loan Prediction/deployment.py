import streamlit as st
import requests
import joblib
from streamlit_lottie import st_lottie
import numpy as np

st.set_page_config(page_title='Personal Loan Bank', page_icon='::star::')

def load_lottie(url): # test url if you want to use your own lottie file 'valid url' or 'invalid url'
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def prepare_input_data_for_model(Income,Family,CCAvg,Education,Mortgage,Securities_Account,CD_Account):
    #sex = gender.map(gen)
    if Education== 'Undergrad':
        e = 1
    elif Education== 'Graduate':
        e = 2
    else:
        e=3
    
    #s_b = ssc_b.map(sb)
    if Securities_Account == 'Yes':
        c = 1
    else:
        c = 0
    #h_b = hsc_b.map(hb)
    if CD_Account == 'Yes':
        a = 1
    else:
        a = 0
    #'Income', 'Family', 'CCAvg','Education', 'Mortgage', 'Securities Account','CD Account', 
    A = [Income,Family,CCAvg,e,Mortgage,c,a]
    sample = np.array(A).reshape(-1,len(A))
    
    return sample



loaded_model = joblib.load(open("myfile", 'rb'))

st.write('# Personal Loan Bank Deployment')
lottie_link ="https://assets8.lottiefiles.com/packages/lf20_ax5yuc0o.json"
animation = load_lottie(lottie_link)

st.write('---')
st.subheader('Enter your details to predict your loan status')

with st.container():
    
    right_column, left_column = st.columns(2)
    #'Income', 'Family', 'CCAvg','Education', 'Mortgage', 'Securities Account','CD Account', 
    with right_column:
        
        Income= st.number_input('Income : ', step=0.1)
        
        Family= st.number_input('Family size : ', step=0.1)
        
        CCAvg= st.number_input('Avg. spending on credit cards per month ($000) : ', step=0.1)

        Mortgage= st.number_input('Value of mortgage : ', step=0.1)
        
        Education= st.selectbox('Education: ', ('Undergrad', 'Graduate', 'Advanced/Professional'))
        
        Securities_Account=st.radio('Do you have security account with the bank? ',['Yes','No'])
        
        CD_Account=st.radio('Do you have a certificate of deposit (CD) account with the bank? ',['Yes','No'])
        
        sample = prepare_input_data_for_model(Income,Family,CCAvg,Education,Mortgage,Securities_Account,CD_Account)
        

    with left_column:
        st_lottie(animation, speed=1, height=400, key="initial")
        

    if st.button('Predict'):
            pred_Y = loaded_model.predict(sample)
            
            if pred_Y == 1:
                #st.write("## Predicted Status : ", result)
                st.write('### Congratulations ', '!! You get a loan.')
                st.balloons()
            else:
                st.write('### Sorry ', '!! You do not get a loan.')