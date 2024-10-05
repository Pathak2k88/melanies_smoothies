# Import python packages
import streamlit as st
import pandas as pd
import numpy as np
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched

# Write directly to the app
st.title("Pending Smoothie Order:balloon:")
st.write(
    """
    Order that needs to be filled!
    """
    
)
cnx=st.connection("snowflake")
session = cnx.session()
#name_on_order=st.text_input('Name on Smoothie:')
#st.write('Name on your smoothie will be',name_on_order)
#session = get_active_session()
my_dataframe = session.table("smoothies.public.ORDERS").filter(col('INGREDIENTS'),col('NAME_ON_ORDER'),col('ORDER_FILLED'),col('ORDER_UID'))
#my_dataframe = session.table("smoothies.public.ORDERS").filter(col('ORDER_FILLED'))
#ingredients_list = st.multiselect("Choose upto 5 ingredients",my_dataframe)
st.write(my_dataframe)
editable_df = st.data_editor(my_dataframe)
submitted = st.button('Submit')
if submitted:
    #st.success('Someone clicked the button', icon = '👍')
    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)
    try:
        og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )    
        st.success('Orders Updated',icon = '👍')
    except:
        st.write('something went wrong')
else:
    st.success('There are no pending orders',icon = '👍')
        
   
