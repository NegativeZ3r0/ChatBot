import streamlit as st
import json
import os
import google.generativeai as genai


st.set_page_config(page_title="Dororo AI", page_icon="images/logo.png", layout="centered", initial_sidebar_state="auto") # Srujan choose this "Dororo AI" name
st.logo("images/banner.png", icon_image="images/logo.png")

GOOGLE_API_KEY = "*****************************" # Replace with Google_Api_Key 
genai.configure(api_key=GOOGLE_API_KEY)
geminiModel=genai.GenerativeModel("gemini-1.5-flash") 
chat = geminiModel.start_chat(history=[])


if "history" not in st.session_state:
    st.session_state.history: list[dict] = []   # List for storing history messages

if "messages" not in st.session_state:
    st.session_state.messages: list[dict] = []   # List to store messages for main page


# Main page
def ChatBot() -> None:
    ''' Stuff you see on Main page '''
    st.header("✨ Dororo AI", divider="orange")
    st.subheader(" Ask Dororo AI anything ")

    sidebar()

    for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# how can i display hello world on terminal using rust?
    # Chat 
    prompt: str = st.chat_input("Message Dodoro...")
    if prompt:
        with st.chat_message("user"):
            st.markdown(f"You: {prompt}")

        st.session_state.messages.append({"role": "user", "content": f"You: {prompt}"})

        response = chat.send_message(prompt)
        response = f"Dororo: \n{response.text}"

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

        st.session_state.history.extend(st.session_state.messages)


def sidebar() -> None:
    ''' Stuff you see in the sidebar on the main page '''
    if "creativity" not in st.session_state:
        st.session_state["creativity"]: dict = 1

    st.session_state["creativity"] = st.sidebar.slider(label="**Creativity**", 
                                                        min_value=1, max_value= 5, 
                                                        value=st.session_state["creativity"], 
                                                        help="This increases creativity of responce but also decreases accuracy")
    
    if st.sidebar.button("Clear", use_container_width=True):
        st.session_state.messages.clear()


# History page
def history() -> None:
    ''' Stuff you see on History page '''
    st.header("🕔 History", divider="red")

    # Sidebar for history page
    if st.sidebar.button("Delete", use_container_width=True):
        st.session_state.history.clear()
        st.session_state.messages.clear()

    if st.session_state.history:
        # Display Chat stored in st.session_state.history
        for message in st.session_state.history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        st.subheader("Nothing to show.")


# Pages
pages: list = []
main_page = st.Page(ChatBot, title="Dororo AI", icon=":material/add_circle:")
history_page = st.Page(history, title="History", icon=":material/add_circle:")
pages.extend([main_page, history_page])

pg = st.navigation(pages=pages)
pg.run()
