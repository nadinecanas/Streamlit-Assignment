import streamlit as st

st.title("Simple Streamlit Demo Item I")

st.header("User Information Form")

name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=0, max_value=120, step=1)

if name and age:
    st.write(f"Hello, **{name}**! 👋")
    st.write(f"You are **{int(age)}** years old.")
 
st.header("Fun Fact")

if age:
    years_until_100 = 100 - age
    if years_until_100 > 0:
        st.write(f"You will turn 100 in **{int(years_until_100)}** years!")
    else:
        st.write("Wow! You are already 100 or older! 🎉")
