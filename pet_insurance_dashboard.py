import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Pet Insurance Analytics Dashboard",layout="wide")
st.title("Pet Insurance Problems & Limitations Dashboard")

@st.cache_data
def load_csv(p):
    try:return pd.read_csv(p)
    except:return pd.DataFrame()

vet=load_csv("data/vet_costs.csv")
claims=load_csv("data/claims_data.csv")
complaints=load_csv("data/complaint_data.csv")
appa=load_csv("data/appa_pet_spending.csv")
state=load_csv("data/state_penetration.csv")

c1,c2,c3,c4=st.columns(4)
c1.metric("Insurance Penetration","4.27%")
c2.metric("Uninsured Pets","95.73%")
c3.metric("Insured Pets","7.6M")
c4.metric("Cat Coverage","2.29%")

fig=px.pie(values=[4.27,95.73],names=["Insured","Uninsured"],hole=.6,title="Protection Gap")
st.plotly_chart(fig,use_container_width=True)

market=pd.DataFrame({"Year":[2021,2022,2023,2024,2025],"PremiumGrowth":[12,15,18,20.8,20.8],"EnrollmentGrowth":[10,11,14,16,9]})
fig=make_subplots(specs=[[{"secondary_y":True}]])
fig.add_scatter(x=market.Year,y=market.PremiumGrowth,name='Premium Growth')
fig.add_scatter(x=market.Year,y=market.EnrollmentGrowth,name='Enrollment Growth')
st.plotly_chart(fig,use_container_width=True)

fig=px.bar(pd.DataFrame({"Pet":["Dogs","Cats"],"Penetration":[5.99,2.29]}),x='Pet',y='Penetration',color='Pet',title='Dog vs Cat')
st.plotly_chart(fig,use_container_width=True)

if not appa.empty:
 st.plotly_chart(px.line(appa,x='Year',y='PetHouseholds',title='Pet Ownership Growth'),use_container_width=True)

if not vet.empty:
 b=vet.groupby('Breed',as_index=False)['AnnualVetCost'].mean()
 st.plotly_chart(px.bar(b,x='Breed',y='AnnualVetCost',title='Vet Cost by Breed'),use_container_width=True)

if not claims.empty:
 claims['ROI']=claims['ClaimPaid']-claims['PremiumPaid']
 r=claims.groupby('Breed',as_index=False)['ROI'].mean()
 st.plotly_chart(px.bar(r,x='Breed',y='ROI',title='ROI Analysis'),use_container_width=True)

if not complaints.empty:
 y=complaints.groupby('Year').size().reset_index(name='Complaints')
 st.plotly_chart(px.line(y,x='Year',y='Complaints',title='Complaint Trend'),use_container_width=True)

if not state.empty:
 st.plotly_chart(px.choropleth(state,locations='StateCode',locationmode='USA-states',color='InsuredRate',scope='usa'),use_container_width=True)

fig=go.Figure(go.Scatterpolar(r=[9,8,7,9,7,6],theta=['Affordability','Claim Denials','Coverage Caps','Exclusions','Waiting Periods','Age Restrictions'],fill='toself'))
st.plotly_chart(fig,use_container_width=True)
