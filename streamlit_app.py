# Import python packages
import streamlit as st
import pandas as pd
import numpy as np
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session = cnx.session()


# Write directly to the app
st.title("Customise your Smoothie:balloon:")
st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """
    
)
name_on_order=st.text_input('Name on Smoothie:')
st.write('Name on your smoothie will be',name_on_order)
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect("Choose upto 5 ingredients",my_dataframe,max_selections=6)
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
ingredients_string =''
for x in ingredients_list:
    ingredients_string += x+ ' '
st.write(ingredients_string)
my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
st.write(my_insert_stmt)
#st.stop()
time_to_insert = st.button('Submit Order')
#st.write(my_insert_stmt)
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response)
fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
