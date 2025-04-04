import streamlit as st
import pandas as pd
import altair as alt
def load_data():
    df = pd.read_csv("Chocosales.csv")
    # convert date column to datetime datatype
    df.Date= pd.to_datetime(df.Date, format='%d-%b-%y')
    # convert the amount col to float datatype
    df.Amount = df.Amount.str.replace('$','').str.replace(',','').str.strip().astype('float')
    df['price/box'] =round(df.Amount/df['Boxes Shipped'],2)
    return df

df = load_data()
# App title
st.title('ChocoSales.App')

# create filters
filters={'Sales Person':df['Sales Person'].unique(),
        'Country': df['Country'].unique(),
        'Product': df['Product'].unique(),
        }

# store user selection
selected_filters={}

# generate multi selected widgets dynamically
for key,options in filters.items():
    selected_filters[key] = st.sidebar.multiselect(f'Filter by {key}', options)


# lets have the full data
filtered_df = df.copy()

# apply filter selection to the data
for key,selected_values in selected_filters.items():
    if selected_values:
        filtered_df = filtered_df[filtered_df[key].isin(selected_values)]
    
# display the data
    st.dataframe(df.head())


# calculations
no_of_Transactions= len(filtered_df)
total_revenue = filtered_df['Amount'].sum()
total_boxes = filtered_df['Boxes Shipped'].sum()
no_of_products = filtered_df['Product'].nunique()

# streamlot column component
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric('Transaction', no_of_Transactions)
with col2:
    st.metric('Total Revenue', total_revenue) 
with col3:
    st.metric('Total Boxes', total_boxes)
with col4:
    st.metric('Product', no_of_products)

# charts
st.subheader('Product with the largest revenue')

top_products = filtered_df.groupby('Product')['Amount'].sum().nlargest(5).reset_index()

st.write(top_products)

# altair plotting library
st.subheader('Top five Products by revenue')
# configure bar chart
Chart1 = alt.Chart(top_products).mark_bar().encode(
    x=alt.X('Amount:Q', title='Revenue ($)'),
    y=alt.Y('Product:N'),
    color=alt.Color('Product:N',legend=None)
).properties(height = 300)

# display the chart
st.altair_chart(Chart1, use_container_width = True)
   

