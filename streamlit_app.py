# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name of Smoothie:")
st.write("The name of your smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

#option = st.selectbox(
   # "What is your favorite fruit?",
    #("Banana", "Strawbarries", "Peaches"),
#)

#st.write("You selected:", option)



#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:',
                                  my_dataframe,
                                  max_selections=5)
ingredients_string=''

if ingredients_list:
   # st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''

for each_fruit in ingredients_list:
    ingredients_string += each_fruit+' '
    st.subheader(each_fruit + 'Nutrition Information')
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+each_fruit)
    fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

#st.write(ingredients_list)
#st.write(ingredients_string)


if ingredients_list !=' ':
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+ name_on_order +"""')"""
#st.write(my_insert_stmt)
time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

