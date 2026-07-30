import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import streamlit as st
from sklearn.datasets import load_iris
import pickle

#LOAD DATASET
data= load_iris()
df= pd.DataFrame(data['data'], columns= data['feature_names'])
df['target']= data['target']
classes= data['target_names']

X= df.iloc[:,:-1]

#MODEL LIST
all_model_name= ['Logistic Regression', 'Naive Bayes', 'Decision Tree',  'Random Forest', 'SVM', 'KNN']

all_model=[]

for i in all_model_name:
    file_name= i+'.pkl'
    with open(f"{file_name}", 'rb')as f:
        model= pickle.load(f)
        all_models.append(model)
        
#USED INPUT AND PASTE TITLE
st.title("ML Flower Classsification Project")
#import url
url="https://k3-production-bucket.s3.amazonaws.com/uploads/cD6ccKKMJJW8rENfe_51518iris%20img1.png"
st.image(url)

#show dataframe sample
st.dataframe(df.sample(5))

#LEFT SIDE BAR for USER VALUE INPUT
st.sidebar.title("Select Iris Features")
st.sidebar.img(url)

user_input=[]
for i in x:
    min_i=x[i].min()
    max_i=x[i].max()
    ans=float(st.sidebar.slider(f"Select value of {i}:", min_value= min_i, max_value=max_i))
    
    user_input.append(ans)
    
#USER INPUT SHOW
st.markdown("""<h2> User Input Value </h2>
""",unsafe_allow_html= True)
st.write(user_input)

#MODEL PREDICTION
if st.button("Click here to Predict"):
    with st.spinner("Predicting....")
         input time
         time,sleep(2)
        counter= 0
        model_ans=[]
        model_prob=[]
          for model in all_models:
                ans= model.predict([user_input])[0]
                prob= model.predict_proba([user_input]).max()
                model_prob.append(prob)
                class_ans= classes[ans]
                model_ans.append(class_ans)
                #st.write(f"Prediction by: {all_model_name[counter]}===>{class_ans}")
                counter +=1        
                
        st.markdown("""
        <h2> Model Comparison </h2>
        """,unsafe_allow_html= True)

        comp_df=pd.DataFrame("x":all_model_name, "y":model_prob, 
                             "Model Prediction": class_ans)
        
        import altair as alt
        chart= alt.chart((comp_df).mark_bar().encode( x= 'x', y= 'y', 
                                                     tooltip=['x','y','Model Prediction']))
        
        st.alter_chart(chart, use_container_width= True)
        
        st.markdown("""
        <h2> Final Prediction </h2>
        """,unsafe_allow_html= True)

        data= pd.Series(model_ans)
        final_ans= data.mode().values[0]
        st.success(final_ans)

footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f1f1f1;
    color: #333333;
    text-align: center;
    padding: 10px;
    font-size: 14px;
}
</style>
<div class="footer">
    <p>Made with ❤️ using Streamlit by Jyoti Shokeen</p>
</div>
"""

# Render the footer
st.markdown(footer, unsafe_allow_html=True)

st.markdown(""" Jyoti flower project
""",unsafe_allow_html= True)
