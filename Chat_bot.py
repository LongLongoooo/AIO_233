import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
import os

# File to store user credentials
USER_INFO_FILE = "info.txt"


def save_user_info(email, password):
    with open(USER_INFO_FILE, "a") as file:
        file.write(f"{email}:{password}\n")


def load_user_info():
    if not os.path.exists(USER_INFO_FILE):
        return {}
    with open(USER_INFO_FILE, "r") as file:
        lines = file.readlines()
    user_db = {}
    for line in lines:
        email, password = line.strip().split(":")
        user_db[email] = password
    return user_db


st.title("Basic ChatBot")

# Sidebar for Sign-Up and Login
with st.sidebar:
    st.title("HugChat Authentication")

    # Tabs for Sign-Up and Login
    auth_mode = st.radio("Select Mode", ["Sign-Up", "Login"])

    if auth_mode == "Sign-Up":
        st.subheader("Sign-Up")
        sign_up_email = st.text_input("Enter E-mail", key="sign_up_email")
        sign_up_pass = st.text_input("Enter Password", type="password", key="sign_up_pass")
        sign_up_pass_confirm = st.text_input("Confirm Password", type="password", key="sign_up_pass_confirm")

        if st.button("Sign Up"):
            user_db = load_user_info()
            if sign_up_email in user_db:
                st.warning("User already exists. Please login.")
            elif sign_up_pass != sign_up_pass_confirm:
                st.error("Passwords do not match.")
            else:
                save_user_info(sign_up_email, sign_up_pass)
                st.success("Sign-Up successful. Please login.")

    elif auth_mode == "Login":
        st.subheader("Login")
        hf_email = st.text_input("Enter E-mail", key="login_email")
        hf_pass = st.text_input("Enter Password", type="password", key="login_pass")

        if st.button("Login"):
            user_db = load_user_info()
            if hf_email in user_db and user_db[hf_email] == hf_pass:
                st.session_state.logged_in = True
                st.session_state.email = hf_email
                st.session_state.password = hf_pass
                st.success("Login successful. Proceed to entering your prompt message!")
            else:
                st.error("Invalid username or password")

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def generate_response(prompt_input, email, passwd):
    try:
        sign = Login(email, passwd)
        cookies = sign.login()
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        return chatbot.chat(prompt_input)
    except Exception as e:
        st.error(f"Login failed: {e}")
        return "Error: Unable to generate response due to login failure."


# Check if user is logged in
if st.session_state.get("logged_in", False):
    if prompt := st.chat_input(disabled=False):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(prompt, st.session_state.email, st.session_state.password)
                    st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.write("Please sign-up or login to use the chat.")
