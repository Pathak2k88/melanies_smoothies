# Import python packages
import streamlit as st
import pandas as pd
import numpy as np
import requests
import pandas as pd
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

ingredients_list = st.multiselect("Choose upto 5 ingredients",my_dataframe,max_selections=6)
#st.dataframe(data=my_dataframe,use_container_width=True)
#st.stop()
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string =''
    for x in ingredients_list:
        ingredients_string += x+ ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == x, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', x,' is ', search_on, '.')
        st.subheader(x+' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    
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

#st.text(fruityvice_response)

