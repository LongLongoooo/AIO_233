import streamlit as st
options = st.multiselect("Your favorite colors:", ["Green", "Yellow", "Red", "Blue"], ["Yellow", "Red"])

st.write("You selected:", options)

st.session_state.username = ""
with st.form("Information"):
    col1, col2 = st.columns(2)
    f_name = col1.text_input("First Name")
    l_name = col2.text_input("Last Name")
    submitted = st.form_submit_button("Submit")
    # st.session_state.username = st.text_input("Username", st.session_state.username)
    # submit = st.form_submit_button("Submit name")

if submitted:
    st.write("First Name", f_name)
    st.write("Last Name", l_name)

uploaded_files = st.file_uploader("Choose file", accept_multiple_files=True)